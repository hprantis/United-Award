# //div[@class="app-components-Shopping-PriceCard-styles__priceValue--21Ki_"]

# //div[@class="app-components-Shopping-PriceCard-styles__top--2IU8G"]/div[3]/div/div   #miles

# //div[@class="app-components-Shopping-PriceCard-styles__top--2IU8G"]  # parent
import multiprocessing
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from multiprocessing import Pool, Value, Lock
from functools import partial
import os
import pandas as pd
from calendar import monthrange
import time

df = pd.read_csv("UnitedAirports.csv")
IATA = df.IATA

gecko_path = r"C:\Users\henry\Downloads\geckodriver-v0.31.0-win64\geckodriver.exe"


def init_globals(counter):
    global cnt
    cnt = counter


def init(l):
    global lock
    lock = l


def increment_date(date):
    day = int(date[8:])
    month = int(date[5:7])
    year = int(date[:4])

    if day == monthrange(year, month)[1]:
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        day = 0
    day += 1
    if day < 10:
        date = str(year) + "-" + str(month) + "-0" + str(day)
    if month < 10:
        date = str(year) + "-0" + str(month) + "-" + str(day)
    if month < 10 and day < 10:
        date = str(year) + "-0" + str(month) + "-0" + str(day)
    if month >= 10 and day >= 10:
        date = str(year) + "-" + str(month) + "-" + str(day)

    return date


def award(destination, date):
    website = "https://www.united.com/en/us/fsr/choose-flights?f=BOS&t=" + destination + "&d=" + date + \
              "&tt=1&at=1&sc=7&px=1&taxng=1&newHP=True&clm=30&s=bestmatches"

    options = Options()
    options.headless = True
    service = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(website)
    driver.implicitly_wait(4)

    try:
        try:
            awards = driver.find_element(By.XPATH,
                                        '//div[@class="app-components-Shopping-PriceCard-styles__discountLabel--3JlN9'
                                        '"]/span')
        except NoSuchElementException:
            awards = ""
        #finally:
            #awards = ""
        # if len(awards) > 1:
        # print("Award flights available from BOS to " + destination + " on " + date)
        # a_list.append("BOS to " + destination + " on " + date)  # date + " BOS to " + destination

        if awards != "":
            print("Award flights available from BOS to " + destination + " on " + date)

        # with cnt.get_lock():
        # cnt.value += 1
        # print(cnt.value)

    finally:
        driver.quit()


if __name__ == "__main__":

    '''
    cnt = Value('i', 1)
    flight_date = "2022-08-16"
    date_list = []

    for i in range(0):
        flight_date = increment_date(flight_date)
        date_list.append(flight_date)

    pool = Pool(os.cpu_count() - 1, initializer=init_globals, initargs=(cnt,))
    func = partial(award, "LAX")
    pool.map(func, date_list)
    pool.close()
    pool.join()
    '''
    for i in range(1):
        start = time.time()
        award("CHS", "2022-09-14")
        end = time.time()
        print(end - start)
# initializer=init, initargs=(l,)
# initializer=init_globals, initargs=(cnt,)
