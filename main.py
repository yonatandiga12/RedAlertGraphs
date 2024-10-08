from selenium.webdriver.support import expected_conditions as EC

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

import csv
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

##############
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from AddingData import getPageContentNewWay
########


from dashApp import startApp

DATE_INDEX = 0
CITY_INDEX = 1
HOUR_INDEX = 2
MINUTES_INDEX = 3


def extractListFromString(citiesNames):
    # for cityArea in citiesNames.split(", "):
    #    city = cityArea.split("-")
    #    print(city[0])

    result = set([cityArea.split("-")[0].strip() for cityArea in citiesNames.split(", ")])
    return result


def findDate(element, lastDate, lastHour, lastMinute, time):
    parent = element.find_parent('div', class_='alert_table alert_type_1 no_bottom_border')
    # text = parent.next_sibling.text

    splitTime = time.split(":")
    hour = splitTime[0]
    minutes = splitTime[1]

    # If no date:
    if parent is None:
        if hour <= lastHour:
            return lastDate, hour, minutes
        else:  # Ask the user to enter the date
            date = input(f'\nLast valid time is : {lastDate}, {lastHour}:{lastMinute}.\n'
                         f'Curr time of the alarm is : {hour}:{minutes}.\n'
                         f'Please enter the date of the alarm.:')
            return date, hour, minutes

    text = parent.previous_sibling.text
    if text is None:
        print('Date not found')
        return lastDate, hour, minutes

    dateFound = text[-10:]
    for letter in dateFound:  # check if the date is valid, should be without letters!
        if letter not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            return lastDate, hour, minutes
    return dateFound, hour, minutes


def firstSettingsToDB():
    file = open('C:\\Fun projects\\RedAlert\\RedAlertGraphs\\csv\\csvFile', 'a', encoding='UTF8')
    writer = csv.writer(file)
    # header = ['date', 'city', 'hour', 'minutes']
    # writer.writerow(header)
    writer.writerow([])
    return file, writer


# This function writes all the history to the DB
def writeToDB(rowsToSave, file, writer):
    for row in rowsToSave:
        writer.writerow(row)

    newestDate = f'{rowsToSave[0][DATE_INDEX]} - {rowsToSave[0][HOUR_INDEX]}:{rowsToSave[0][MINUTES_INDEX]}'

    print(f'Done!, added until date and time {newestDate}')



# def getPageContent():
#     URL = "https://www.oref.org.il/12481-he/Pakar.aspx"
#
#     driver = webdriver.Chrome()
#     driver.get(URL)
#
#     # driver.find("li", {"id": "lastweek"}).click()
#     driver.find_element(By.ID, 'lastweek')
#     # driver.find_element_by_id('lastweek').click()
#     #sleep(20)
#
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     driver.close()
#
#     results = soup.find(id="ahNotifications")
#     # print(results.prettify())
#
#     elements = results.find_all('div', attrs={'class': lambda e: e.startswith('alertDetails') if e else False})
#
#     rowsToSave = list()
#     lastDate = ""
#     lastHour = ""
#     lastMinute = ""
#     file, writer = firstSettingsToDB()
#
#     for element in elements:
#         text = element.find("h5")
#         citiesNames = text.next_sibling
#         time = text.text
#
#         date, hour, minutes = findDate(element, lastDate, lastHour, lastMinute, time)
#
#         lastMinute = minutes
#         lastHour = hour
#         if lastDate != date and len(rowsToSave) > 0:
#             writeToDB(rowsToSave, file, writer)
#             rowsToSave = list()
#
#         lastDate = date
#
#         citiesList = extractListFromString(citiesNames)
#
#         for city in citiesList:
#             row = [date, city, hour, minutes]
#             rowsToSave.append(row)
#
#     # Create another function to add rows to DB without deleting all the previous data!
#     # just check what is the last date and hour inserted to the csv file and put the new data until this moment.
#
#     if len(rowsToSave) > 0:
#         writeToDB(rowsToSave, file, writer)
#
#     file.close()


# Moved to a different file
# def getPageContentNewWay():
#     # Define the API URL
#
#     #Added data until 15.10 including!
#     #After all is done, replace in the csv file all the " with blank
#
#     startingDate = "07.10.2023"
#     endingDate = "07.10.2023"
#     api_url = f"https://alerts-history.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&fromDate={startingDate}&toDate={endingDate}&mode=0 "
#
#     file_rocket, writer_rocket = firstSettingsToDB2('rockets_missiles.csv')
#     file_aircraft, writer_aircraft = firstSettingsToDB2('aircraft_intrusions.csv')
#     file_terrorists, writer_terrorists = firstSettingsToDB2('terrorists_intrusions.csv')
#
#     try:
#         # Fetch the data from the API
#         response = requests.get(api_url)
#         response.raise_for_status()  # Check for request errors
#
#         # Parse the JSON response
#         data = response.json()
#
#         inputStr = input(f'The number of alerts is: {len(data)}, do you wish to stop? ')
#         if len(data) > 1980 or inputStr.lower() == 'p':
#             print("Missing data, choose different dates")
#             return
#
#         # Lists to hold alerts
#         rockets = []
#         aircraft = []
#         terrorists = []
#
#         # Iterate over the items in the JSON response
#         for index in range(len(data) - 1, 0, -1):
#             item = data[index]
#             date = item.get('date', '')
#             timeOfAlarm = item.get('time', '')
#             splittedTime = timeOfAlarm.split(':')
#             hour = splittedTime[0]
#             minutes = splittedTime[1]
#             cityName = item.get('data', '')
#             if '"' in cityName:
#                 print()
#             category = item.get('category', '')
#
#             row = [date, cityName, hour, minutes]
#             # Divide data based on category number
#             # Assuming rockets and missiles are category 1, and aircraft penetration is category 2
#             if category == 1:
#                 rockets.append(row)
#             elif category == 2:
#                 aircraft.append(row)
#             elif category == 10:
#                 terrorists.append(row)
#             else:
#                 print(f"Unknown category, {item}")
#
#         # Final write for any remaining data
#         if rockets:
#             writeToDB(rockets, file_rocket, writer_rocket)
#
#         if aircraft:
#             writeToDB(aircraft, file_aircraft, writer_aircraft)
#
#         if terrorists:
#             writeToDB(terrorists, file_terrorists, writer_terrorists)
#
#         print("Alerts have been successfully saved into CSV files.")
#
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to fetch alerts: {e}")


DATE_COLUMN_NAME = "date"
CITY_COLUMN_NAME = "city"
HOUR_COLUMN_NAME = "hour"
MINUTES_COLUMN_NAME = "minutes"
TABLE_NAME = "csvUntil41123"


def printNumOfRows(cursor):
    sqlite_select_query = f"""SELECT * from {TABLE_NAME}"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))


# My Version for Histogram
def showMinutesColumns(cursor):
    # sqlite_select_query = f"""SELECT COUNT({MINUTES_COLUMN_NAME}), {MINUTES_COLUMN_NAME}
    #                           FROM {TABLE_NAME}
    #                           WHERE not {DATE_COLUMN_NAME} = '07.10.2023'
    #                           GROUP BY {MINUTES_COLUMN_NAME}   """

    sqlite_select_query = f"""SELECT COUNT({MINUTES_COLUMN_NAME}), {MINUTES_COLUMN_NAME}
                              FROM {TABLE_NAME}
                              GROUP BY {MINUTES_COLUMN_NAME}   """
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    y = [record[0] for record in records]
    x = [record[1] for record in records]

    plt.figure(figsize=(12, 6))

    # Plotting Line Graph
    plt.title("Number of Alerts in a specific Minute (With 7.10)")
    plt.xlabel('Minute')
    plt.ylabel("Num of alerts")

    plt.xticks(np.arange(0, 60, 5))
    plt.yticks(np.arange(0, max(y), 50))
    plt.bar(x, y, color='blue', width=0.8)

    # Saving a plotted graph as an Image
    plt.savefig('minutesGraph (With 7-10).png')
    plt.show()


# Utilizes the Histogram in matplotlib
def hoursHist(cursor):
    sqlite_select_query = f"""SELECT {HOUR_COLUMN_NAME} from {TABLE_NAME}
                              WHERE not {DATE_COLUMN_NAME} = '07.10.2023' """
    # sqlite_select_query = f"""SELECT {HOUR_COLUMN_NAME} from {TABLE_NAME} """

    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    x = [r[0] for r in records]

    plt.figure(figsize=(12, 6))

    # Plotting Line Graph
    plt.title("Number of Alerts in a specific Hour")
    plt.xlabel('Hour')
    plt.ylabel("Num of alerts")
    plt.hist(x, 24, color='blue', width=0.8)
    plt.xticks(np.arange(0, 24))
    plt.savefig('hourGraph.png')
    plt.show()


def plotGraphs():
    global sqliteConnection
    try:
        # sqliteConnection = sqlite3.connect('alerts.db')
        sqliteConnection = sqlite3.connect('csv\\alerts.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # printNumOfRows(cursor)

        showMinutesColumns(cursor)
        # hoursHist(cursor)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


if __name__ == "__main__":
    getPageContentNewWay()
    # getPageContent()
    #plotGraphs()
    #startApp()
