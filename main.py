import csv
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

DATE_INDEX = 0
CITY_INDEX = 1
HOUR_INDEX = 2
MINUTES_INDEX = 3

def extractListFromString(citiesNames):
    #for cityArea in citiesNames.split(", "):
    #    city = cityArea.split("-")
    #    print(city[0])

    result = set([cityArea.split("-")[0].strip() for cityArea in citiesNames.split(", ")])
    return result


def findDate(element, lastDate, lastHour, lastMinute, time):
    parent = element.find_parent('div', class_='alert_table alert_type_1 no_bottom_border')
    #text = parent.next_sibling.text

    splitTime = time.split(":")
    hour = splitTime[0]
    minutes = splitTime[1]

    #If no date:
    if parent is None:
        if hour <= lastHour:
            return lastDate, hour, minutes
        else:  #Ask the user to enter the date
            date = input(f'\nLast valid time is : {lastDate}, {lastHour}:{lastMinute}.\n'
                         f'Curr time of the alarm is : {hour}:{minutes}.\n'
                         f'Please enter the date of the alarm.:')
            return date, hour, minutes

    text = parent.previous_sibling.text
    if text is None:
        print('Date not found')
        return "-1"

    return text[-10:], hour, minutes


#This function writes all the history to the DB
def writeToDB(rowsToSave):
    file = open('C:\\Fun projects\\RedAlert\\RedAlertGraphs\\csvFile', 'w', encoding='UTF8')
    writer = csv.writer(file)
    header = ['date', 'city', 'hour', 'minutes']
    writer.writerow(header)

    for row in reversed(rowsToSave):
        writer.writerow(row)

    newestDate = f'{rowsToSave[0][DATE_INDEX]} - {rowsToSave[0][HOUR_INDEX]}:{rowsToSave[0][MINUTES_INDEX]}'

    print(f'Done!, added until date and time {newestDate}')

    file.close()


def getPageContent():

    URL = "https://www.oref.org.il/12481-he/Pakar.aspx"

    driver = webdriver.Chrome()
    driver.get(URL)

    #driver.find("li", {"id": "lastweek"}).click()
    driver.find_element(By.ID, 'lastweek')
    #driver.find_element_by_id('lastweek').click()
    sleep(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    results = soup.find(id="ahNotifications")
    #print(results.prettify())

    elements = results.find_all('div', attrs={'class': lambda e: e.startswith('alertDetails') if e else False})

    rowsToSave = list()
    lastDate = ""
    lastHour = ""
    lastMinute = ""

    for element in elements:
        text = element.find("h5")
        citiesNames = text.next_sibling
        time = text.text

        date, hour, minutes = findDate(element, lastDate, lastHour, lastMinute, time)

        lastMinute = minutes
        lastHour = hour
        lastDate = date

        citiesList = extractListFromString(citiesNames)

        for city in citiesList:
            row = [date, city, hour, minutes]
            rowsToSave.append(row)

    #Create another function to add rows to DB without deleting all the previous data!
    #just check what is the last date and hour inserted to the csv file and put the new data until this moment.

    writeToDB(rowsToSave)






if __name__ == "__main__":
    getPageContent()
