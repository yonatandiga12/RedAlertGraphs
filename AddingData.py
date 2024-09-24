import sqlite3

import csv
import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime, timedelta

#Dat until 23.9.24

DATE_INDEX = 0
CITY_INDEX = 1
HOUR_INDEX = 2
MINUTES_INDEX = 3

PATH_TO_DB = 'csv\\newData\\'
DB_NAME = 'alerts.db'
TERRORISTS_TABLE_NAME = 'terrorists'
ROCKETS_TABLE_NAME = 'missiles'
AIRCRAFT_TABLE_NAME = 'aircraft'
SQL_DATE_COLUMN_NAME = 'dates'
SQL_HOUR_COLUMN_NAME = 'hour'
SQL_MINUTES_COLUMN_NAME = 'minutes'
SQL_CITY_COLUMN_NAME = 'city'

def extractListFromString(citiesNames):
    # for cityArea in citiesNames.split(", "):
    #    city = cityArea.split("-")
    #    print(city[0])

    result = set([cityArea.split("-")[0].strip() for cityArea in citiesNames.split(", ")])
    return result

def firstSettingsToDB2(name):
    path = 'C:\\Fun projects\\RedAlert\\RedAlertGraphs\\csv\\newData\\' + name
    file = open(path, 'a', encoding='UTF8')
    writer = csv.writer(file)
    # header = ['date', 'city', 'hour', 'minutes']
    #writer.writerow(header)
    writer.writerow([])
    return file, writer


# This function writes all the history to the DB
def writeToDB2(rowsToSave, file, writer):
    for row in rowsToSave:
        writer.writerow(row)

    newestDate = f'{rowsToSave[0][DATE_INDEX]} - {rowsToSave[0][HOUR_INDEX]}:{rowsToSave[0][MINUTES_INDEX]}'

    print(f'Done!, added until date and time {newestDate}')


def writeSQLToDB(cursor, listOfRows, tableName):
    for currRow in listOfRows:
        currDate = currRow[DATE_INDEX]
        cityName = currRow[CITY_INDEX]
        hour = currRow[HOUR_INDEX]
        minutes = currRow[MINUTES_INDEX]
        # Insert a new row into the table
        cursor.execute(f'''
            INSERT INTO {tableName} ({SQL_DATE_COLUMN_NAME}, {SQL_CITY_COLUMN_NAME},
            {SQL_HOUR_COLUMN_NAME}, {SQL_MINUTES_COLUMN_NAME}) VALUES (?, ?, ?, ?)''',
                       (currDate, cityName, hour, minutes))


def getPageContentNewWay():
    def fetch_data(startDate, endDate):
        api_url = f"https://alerts-history.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&fromDate={startDate}&toDate={endDate}&mode=0"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch alerts: {e}")
            return None

    def process_data(data, CSVFlag=True):
        if CSVFlag:
            #This is for entering the data to the CSV
            file_rocket, writer_rocket = firstSettingsToDB2('rockets_missiles.csv')
            file_aircraft, writer_aircraft = firstSettingsToDB2('aircraft_intrusions.csv')
            file_terrorists, writer_terrorists = firstSettingsToDB2('terrorists_intrusions.csv')
        else:
            # Connect to the SQLite database (or create it if it doesn't exist)
            conn = sqlite3.connect(PATH_TO_DB + DB_NAME)  # Replace with your database file or connection string
            cursor = conn.cursor()

        rockets = []
        aircraft = []
        terrorists = []

        for index in range(len(data) - 1, 0, -1):
            item = data[index]
            date = item.get('date', '')
            timeOfAlarm = item.get('time', '')
            splittedTime = timeOfAlarm.split(':')
            hour = splittedTime[0]
            minutes = splittedTime[1]
            cities = extractListFromString(item.get('data', ''))
            category = item.get('category', '')
            for cityName in cities:
                row = [date, cityName, hour, minutes]
                if category == 1:
                    rockets.append(row)
                elif category == 2:
                    aircraft.append(row)
                elif category == 10:
                    terrorists.append(row)
                else:
                    print(f"Unknown category, {item}")

        if CSVFlag:
            if rockets:
                writeToDB2(rockets, file_rocket, writer_rocket)
            if aircraft:
                writeToDB2(aircraft, file_aircraft, writer_aircraft)
            if terrorists:
                writeToDB2(terrorists, file_terrorists, writer_terrorists)
        else:
            if rockets:
                writeSQLToDB(cursor, rockets, ROCKETS_TABLE_NAME)
            if aircraft:
                writeSQLToDB(cursor, aircraft, AIRCRAFT_TABLE_NAME)
            if terrorists:
                writeSQLToDB(cursor, terrorists, TERRORISTS_TABLE_NAME)
        if not CSVFlag:
            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            print("Alerts have been successfully saved into the DB.")



    def on_fetch():
        global data
        data = fetch_data(start_date.get(), end_date.get())
        if data:
            result_label.config(text=f"The number of alerts is: {len(data)}")
            continue_button.pack()
            stop_button.pack()
        else:
            result_label.config(text="Failed to fetch data. Please try again.")

    def on_fromStarting():
        startingDate = start_date.get()
        indexOfStart = date_options.index(startingDate)
        dates = date_options[:indexOfStart+1]
        dates.reverse()
        n = 10
        final = [dates[i * n:(i + 1) * n] for i in range((len(dates) + n - 1) // n)]
        for currList in final:
            startingDate = currList[0]
            endingDate = currList[-1]
            dataCurr = fetch_data(startingDate, endingDate)
            if len(dataCurr) > 1990:  #If there were alot of alerts that time
                for oneDate in currList:
                    data1 = fetch_data(oneDate, oneDate)
                    process_data(data1)
            else:
                process_data(dataCurr)

    def on_continue():
        process_data(data)
        #root.destroy()

    def on_stop():
        start_date.set("")
        end_date.set("")
        result_label.config(text="")
        continue_button.pack_forget()
        stop_button.pack_forget()

    root = tk.Tk()
    root.title("Alert Data Fetcher")

    date_options = [(datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y") for i in range(400)]

    tk.Label(root, text="Start Date:").pack()
    start_date = tk.StringVar(root)
    start_date_dropdown = ttk.Combobox(root, textvariable=start_date, values=date_options)
    start_date_dropdown.pack()

    tk.Label(root, text="End Date:").pack()
    end_date = tk.StringVar(root)
    end_date_dropdown = ttk.Combobox(root, textvariable=end_date, values=date_options)
    end_date_dropdown.pack()

    fetch_button = tk.Button(root, text="Fetch Data", command=on_fetch)
    fetch_button.pack()

    fromStartingDateUntilNow_button = tk.Button(root, text="From Starting Date Until Now", command=on_fromStarting)
    fromStartingDateUntilNow_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    continue_button = tk.Button(root, text="Continue", command=on_continue)
    stop_button = tk.Button(root, text="Stop", command=on_stop)

    root.mainloop()
