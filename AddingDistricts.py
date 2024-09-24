import difflib

import csv

# with open('C:\\Fun projects\\RedAlert\\RedAlertGraphs\\csv\\newData\\Cities.csv', "r") as source:
#     reader = csv.reader(source)
#
#     with open("output.csv", "w") as result:
#         writer = csv.writer(result)
#         for r in reader:
#             # Use CSV Index to remove a column from CSV
#             # r[3] = r['year']
#             writer.writerow((r[1], r[3]))


ROCKETS_CSV_NAME = 'rockets_missiles.csv'
AIRCRAFT_CSV_NAME = 'aircraft_intrusions.csv'
CITIES_CSV = 'Cities.csv'
PATH = 'C:\\Fun projects\\RedAlert\\RedAlertGraphs\\csv\\newData\\'


def checkCitiesMatchNameFromAlarms(citiesNames):
    cities = set()
    with open(PATH + ROCKETS_CSV_NAME, mode='r', encoding="utf8") as file:
        csvFile = csv.DictReader(file)
        for lines in csvFile:
            cities.add(lines['city'])

    with open(PATH + AIRCRAFT_CSV_NAME, mode='r', encoding="utf8") as file:
        csvFile = csv.DictReader(file)
        for lines in csvFile:
            cities.add(lines['city'])

    counter = 1
    for city in cities:
        if city not in citiesNames:
            print(f'{counter}) Name from alarmsCSV: {city}')
            counter += 1

            closestMatch = difflib.get_close_matches(city, citiesNames)
            print(f'Closest Match: {closestMatch}\n')

def getNameOfCitiesFromCitiesCSV():
    cities = []

    with open(PATH + CITIES_CSV, mode='r') as file:
        csvFile = csv.DictReader(file)
        for lines in csvFile:
            cities.append(lines['HEBREW_NAME'])

    return cities







if __name__ == "__main__":

    citiesNames1 = getNameOfCitiesFromCitiesCSV()
    checkCitiesMatchNameFromAlarms(citiesNames1)

