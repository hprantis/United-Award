from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

gecko_path = r"C:\Users\henry\Downloads\geckodriver-v0.31.0-win64\geckodriver.exe"


def award(date, a_list, dictionary, destination):
    website = "https://www.united.com/en/us/fsr/choose-flights?f=BOS&t=" + destination + "&d=" + date + \
              "&tt=1&at=1&sc=7&px=1&taxng=1&newHP=True&clm=30&s=bestmatches"
    if dictionary[a_list] == "range_list":
        website = "https://www.united.com/en/us/fsr/choose-flights?f=" + destination + "&t=BOS&d=" + date + \
                  "&tt=1&at=1&sc=7&px=1&taxng=1&newHP=True&clm=30&s=bestmatches"

    options = Options()
    options.headless = True
    service = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(website)
    driver.implicitly_wait(6)

    awards = driver.find_elements(By.XPATH,
                                  '//div[@class="app-components-Shopping-PriceCard-styles__discountLabel--3JlN9"]/span')

    if len(awards) > 1:
        if dictionary[a_list] == "award_list":
            print("Award flights available from BOS to " + destination + " on " + date)
        if dictionary[a_list] == "range_list":
            print("Award flights available from " + destination + " to BOS on " + date)
        a_list.append(destination)

    driver.quit()
