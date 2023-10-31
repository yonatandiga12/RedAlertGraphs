import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def extractListFromString(citiesNames):
    return list()


def findDate(element):
    return "12"


def putInDB(date, city, hour, minutes):
    pass


def getPageContent():
    URL = "https://www.oref.org.il/12481-he/Pakar.aspx"

    driver = webdriver.Chrome()
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    results = soup.find(id="ahNotifications")
    #print(results.prettify())

    #elements = results.find_all("div", {"class": "alertDetails more_1_28_10_2023 hdn"})
    elements = results.find_all('div', attrs={'class': lambda e: e.startswith('alertDetails') if e else False})

    for element in elements:
        text = element.find("h5")
        citiesNames = text.next_sibling
        time = text.text

        citiesList = extractListFromString(citiesNames)
        date = findDate(element)
        
        splitTime = time.split(":")
        if len(splitTime) == 2:
            hour = splitTime[0]
            minutes = splitTime[1]
        else:
            print("Something went wrong with the time extraction")
            continue
        
        for city in citiesList:
            putInDB(date, city, hour, minutes)






if __name__ == "__main__":
    getPageContent()
