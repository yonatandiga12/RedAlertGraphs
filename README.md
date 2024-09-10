# RedAlertGraphs
View Red Alert alarms in graphs, including : alarms per hours, per minute and per cities.
      https://yonatandiga12.github.io/RedAlertGraphs/
<br />
<br />

## How to get the data:
1. Run the function getPageContentNewWay() from main. (If you want the data in DB and not CSV, you need to change CSV_FLAG)
2. Choose dates 
3. If you choose From starting date until now, just press it, and it will collect the data
4. If you choose starting and ending date, choose fetch data and then continue.
5. If chosen CSV: Upon finish, Open the csvFile and press "Edit" -> "Line Operations" -> "Remove empty Lines" 
<br />

## How to view the graphs:
1. Run the function startApp() from main.
2. If runs locally go to http://127.0.0.1:8050/.
<br />


## Graph Examples:
<h3 align="center">Number of Alerts in selected cities</h3>
<br />
<br />
<p align="center">
  <img src="https://raw.githubusercontent.com/yonatandiga12/RedAlertGraphs/main/screenshots/screenShot1.jpg" width="1000" title="img1">
</p>
<br />  
<br />  
<h3 align="center">Number of Alerts per Minute</h3>  
<br />
<br />
<p align="center">
  <img src="https://raw.githubusercontent.com/yonatandiga12/RedAlertGraphs/main/screenshots/screenShot2.jpg" width="1000" title="img2">
</p>
<br />  
<br />  
<h3 align="center">Number of Alerts per Hour</h3>  
<br />
<br />
<p align="center">
  <img src="https://raw.githubusercontent.com/yonatandiga12/RedAlertGraphs/main/screenshots/screenShot3.jpg" width="1000" title="img3">
</p>
<br />  
<br />  

<h3 align="center">Number of Alerts in all cities</h3>
<br />
<br />
<p align="center">
  <img src="https://raw.githubusercontent.com/yonatandiga12/RedAlertGraphs/main/screenshots/screenShot4.jpg" width="1000" title="img4">
</p>
<br />  
<br />



## Additional Info:
Data is harvested from : "https://www.oref.org.il/12481-he/Pakar.aspx"

<br />  

NEW WAY:
I got the data from this link : https://alerts-history.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&fromDate={startDate}&toDate={endDate}&mode=0
Just change the starting date and ending date and a json dictionary will return.

OLD WAY:
It was organized through web scarping with Beautiful Soup and Selenium library.

The alarms count is done in this method:
If in the same minute there is more than 1 alarm in 1 city, I will save only 1 alarm in this minute.
If it's not in the same minute it will not count as 1.  
For example: if in 14:00 there were alarms in Beer Sheva North and South, it will be saved as 1 alarm in Beer Sheva.
If there is another alarm in 14:01 in Beer Sheva North, it will be saved as a different alarm.


There may be different numbers in other graphs, depending on the counting system. 
