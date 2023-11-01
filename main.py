import csv

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def extractListFromString(citiesNames):
    #for cityArea in citiesNames.split(", "):
    #    city = cityArea.split("-")
    #    print(city[0])

    result = set([cityArea.split("-")[0].strip() for cityArea in citiesNames.split(", ")])
    return result


def findDate(element):
    # for name in element['class']:
    #     if "more_0" in name:
    #         date = name[7:]
    #         return date
    # return "-1"
    parent = element.find_parent('div', class_='alert_table alert_type_1 no_bottom_border')
    #text = parent.next_sibling.text
    text = parent.previous_sibling.text
    if text is None:
        print('Hi')
    return text[-10:]


def getPageContent():

    URL = "https://www.oref.org.il/12481-he/Pakar.aspx"

    driver = webdriver.Chrome()
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    results = soup.find(id="ahNotifications")
    #print(results.prettify())

    elements = results.find_all('div', attrs={'class': lambda e: e.startswith('alertDetails') if e else False})

    file = open('C:\\Fun projects\\RedAlert\\RedAlertGraphs\\csvFile', 'w+', encoding='UTF8')
    writer = csv.writer(file)
    header = ['date', 'city', 'hour', 'minutes']
    writer.writerow(header)


    for element in elements:
        text = element.find("h5")
        citiesNames = text.next_sibling
        time = text.text

        date = findDate(element)
        # if date == "-1":
        #     print("There is no date!")
        #     continue

        citiesList = extractListFromString(citiesNames)

        splitTime = time.split(":")
        if len(splitTime) == 2:
            hour = splitTime[0]
            minutes = splitTime[1]
        else:
            print("Something went wrong with the time extraction")
            continue

        print(f'{date}  -  {citiesList}, {hour}:{minutes}')

        for city in citiesList:
            row = [date, city, hour, minutes]
            writer.writerow(row)


    file.close()




if __name__ == "__main__":
    getPageContent()
