# TO DO
# Catch exceptions
# Add more detail to round trip availability in awards.txt
# turn counter into percent to completion

# Try multithreading for possible performance improvement
# Write new file to filter UnitedAirports.csv

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from multiprocessing import Pool, Manager, Value
from functools import partial
import os
from calendar import monthrange
import time
from datetime import date

df = pd.read_csv("UnitedAirports.csv")
IATA = df.IATA
airport = df.AIRPORT
state = df.STATE
city = df.CITY

# Needs to be set to geckodriver installation location.
gecko_path = r"C:\Users\henry\Downloads\geckodriver-v0.31.0-win64\geckodriver.exe"


# Counter init for counting between processes.
def init_globals(counter):
    global count
    count = counter


def percent(counter, mode):
    counter_as_percent = "-1"
    if mode == 1:
        counter_as_percent = "{:.2f}".format(counter/206*100) + "%"
    return counter_as_percent


# If an awards text file exits, copy it to the backup file.  Otherwise, create award text file and backup file.
def copy(from_, to):
    path = os.getcwd()
    exists = os.path.exists(path + r"\\" + from_)

    if exists:
        file1 = open(from_, "r")
        var = file1.read()
        file1.close()

        file2 = open(to, "w")
        file2.write(var)
        file2.close()
    else:
        file1 = open(from_, "w")
        file1.close()


# increments date given YYYY-MM-DD format
def increment_date(date_):
    # YYYY-MM-DD
    day = int(date_[8:])
    month = int(date_[5:7])
    year = int(date_[:4])

    if day == monthrange(year, month)[1]:
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        day = 0
    day += 1
    if day < 10:
        date_ = str(year) + "-" + str(month) + "-0" + str(day)
    if month < 10:
        date_ = str(year) + "-0" + str(month) + "-" + str(day)
    if month < 10 and day < 10:
        date_ = str(year) + "-0" + str(month) + "-0" + str(day)
    if month >= 10 and day >= 10:
        date_ = str(year) + "-" + str(month) + "-" + str(day)

    return date_


# Returns the number of days between two dates
def days_to_return_date(depart_date, return_date):
    depart_day = int(depart_date[8:])
    depart_month = int(depart_date[5:7])
    depart_year = int(depart_date[:4])

    return_date = str(int(return_date[:4])) + "-" + str(int(return_date[5:7])) + "-" + str(int(return_date[8:]))
    c = 0
    while depart_date != return_date:
        if depart_day == monthrange(depart_year, depart_month)[1]:
            if depart_month == 12:
                depart_month = 1
                depart_year += 1
            else:
                depart_month += 1
            depart_day = 0
        depart_day += 1
        c += 1
        depart_date = str(depart_year) + "-" + str(depart_month) + "-" + str(depart_day)

    return c


# Enables multiprocessing.
def multi_processing(function, date_, a_list, dictionary, iterable):
    pool = Pool(os.cpu_count() - 1, initializer=init_globals, initargs=(count,))
    func = partial(function, date_, a_list, dictionary)
    pool.map(func, iterable)

    pool.close()
    pool.join()


# Main scraping function, finds award availability.
def award(date_, a_list, dictionary, destination):
    website = "https://www.united.com/en/us/fsr/choose-flights?f=BOS&t=" + destination + "&d=" + date_ + \
              "&tt=1&at=1&sc=7&px=1&taxng=1&newHP=True&clm=30&s=bestmatches"
    if dictionary[a_list] == "return_list":
        website = "https://www.united.com/en/us/fsr/choose-flights?f=" + destination + "&t=BOS&d=" + date_ + \
                  "&tt=1&at=1&sc=7&px=1&taxng=1&newHP=True&clm=30&s=bestmatches"

    options = Options()
    options.headless = True
    service = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(website)
    driver.implicitly_wait(6)

    try:
        awards = driver.find_elements(By.XPATH,
                                      '//div[@class="app-components-Shopping-PriceCard-styles__discountLabel--3JlN9'
                                      '"]/span')
        with count.get_lock():
            count.value += 1

        if len(awards) > 1:
            if dictionary[a_list] == "award_list":
                print(count.value, " Award flights available from BOS to " + destination + " on " + date_)
                a_list.append("BOS to " + destination + " on " + date_)  # date + " BOS to " + destination
            if dictionary[a_list] == "return_list":
                print(count.value, "Award flights available from " + destination + " to BOS on " + date_)
                a_list.append(destination + " to BOS on " + date_)
        else:
            print(count.value)

    finally:
        driver.quit()


# Alternate award function, modifies variable locations for use with mode 5
def award_reverse(destination, a_list, dictionary, date_):
    award(date_, a_list, dictionary, destination)


if __name__ == "__main__":
    start = time.time()

    # files to store output of program
    award_file = "awards.txt"
    backup_file = "backup.txt"

    today = str(date.today())

    # Input variables
    flight_date = "2022-12-20"
    ret_date = "2022-12-22"
    flight_destination = "LAX"  # MODE 5 only
    return_range = 2  # number of days to search for return flights
    trip_length = 2  # offset between outbound and inbound flights
    search_mode = 4
    # MODE 1: single date, search all airports                              206
    # MODE 2: multiple dates, search all airports                           206 * number of dates
    # MODE 3: single date with return range, search all airports            206 + 206 * return range
    # MODE 4: multiple dates with return range, search all airports         206 * number of dates + 206 * return range
    # MODE 5: single destination with return range, search multiple dates   number of dates*2

    manager = Manager()
    # count for program status
    count = Value('i', 0)
    # award_list, return_list store outbound and return award availability
    award_list = manager.list()
    return_list = manager.list()
    # list_dict allows list names to be referenced as variables.
    list_dict = {award_list: "award_list", return_list: "return_list"}

    if search_mode == 1:
        multi_processing(award, flight_date, award_list, list_dict, IATA)

    if search_mode == 2:
        for i in range(days_to_return_date(flight_date, ret_date)):
            flight_date = increment_date(flight_date)
            multi_processing(award, flight_date, award_list, list_dict, IATA)
            print("\n")

    if search_mode == 3:
        multi_processing(award, flight_date, award_list, list_dict, IATA)
        for i in range(return_range):
            flight_date = increment_date(flight_date)
            multi_processing(award, flight_date, return_list, list_dict, award_list)
            print("\n")

    if search_mode == 4:
        temp_date = flight_date
        for i in range(days_to_return_date(flight_date, ret_date)):
            flight_date = increment_date(flight_date)
            multi_processing(award, flight_date, award_list, list_dict, IATA)
            print("\n")

        flight_date = temp_date
        for i in range(trip_length):
            flight_date = increment_date(flight_date)

        for i in range(return_range):
            flight_date = increment_date(flight_date)
            multi_processing(award, flight_date, return_list, list_dict, IATA)
            print("\n")

    if search_mode == 5:
        date_list = []
        for i in range(days_to_return_date(flight_date, ret_date)):
            flight_date = increment_date(flight_date)
            date_list.append(flight_date)

        multi_processing(award_reverse, flight_destination, award_list, list_dict, date_list)

    # If an awards text file exits, copy it to the backup file.  Otherwise, create award text file and backup file.
    copy(award_file, backup_file)
    award_list.sort()

    # Writes data to text file with formatting
    file = open(award_file, "w")

    round_trip_availability = []
    if search_mode == 3 or search_mode == 4:
        award_list_IATA = []
        return_list_IATA = []

        for i in award_list:
            award_list_IATA.append(i[7:10])
        for i in return_list:
            return_list_IATA.append(i[:3])

        for i in award_list_IATA:
            if i in return_list_IATA:
                round_trip_availability.append(i)

    file.write("This data is from " + today + "\n\n")

    file.write("Round trip availability\n\n")
    for i in round_trip_availability:
        file.write("from BOS to " + i + "\n")

    file.write("Outbound flights\n\n")
    for award in award_list:
        file.write(award + "\n")

    file.write("\nReturn flights\n\n")
    for award in return_list:
        file.write(award + "\n")
    file.close()

    # Timer
    end = time.time()
    print(end - start)
