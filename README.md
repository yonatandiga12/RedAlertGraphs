# RedAlertGraphs
Visualize Red Alert alarms in graphs 

To get the data:
1. Run the function getPageContent() from main.
2. Choose dates from the site
3. If it asks for a date, write the last date from the dates chosen. Iit start from the last date backwards.
4. It will print messages of success.

To view graphs:
1. Run the function startApp() from main.
2. If runs locally go to http://127.0.0.1:8050/.


Data is harvested from : "https://www.oref.org.il/12481-he/Pakar.aspx"
It is organized through web scarping with Beautiful Soup and Selenium library.

The alarms count is done in this method:
If in the same minute there is more than 1 alarm in 1 city, I will save only 1 alarm in this minute.
If it's not in the same minute it will not count as 1.
For example: if in 14:00 there were alarms in Beer Sheva North and South, it will be saved as 1 alarm in Beer Sheva.
If there is another alarm in 14:01 in Beer Sheva North, it will be saved as a different alarm.


There may be different numbers in other graphs, depending on the counting system. 
