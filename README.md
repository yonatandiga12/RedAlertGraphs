# RedAlertGraphs
View Red Alert alarms in graphs, including : alarms per hours, per minute and per cities.
<br />
<br />

## How to get the data:
1. Run the function getPageContent() from main.
2. Choose dates from the site
3. If it asks for a date, write the last date from the dates chosen. It starts from the last date backwards.
4. Upon finish, Open the csvFile and save a copy as csvUpdated.csv 
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
It is organized through web scarping with Beautiful Soup and Selenium library.

The alarms count is done in this method:
If in the same minute there is more than 1 alarm in 1 city, I will save only 1 alarm in this minute.
If it's not in the same minute it will not count as 1.  
For example: if in 14:00 there were alarms in Beer Sheva North and South, it will be saved as 1 alarm in Beer Sheva.
If there is another alarm in 14:01 in Beer Sheva North, it will be saved as a different alarm.


There may be different numbers in other graphs, depending on the counting system. 
