# BballRefScraper
Scrapper for basketballreference.com

This repository acts as a scrapper for data from basketballreference.com.
It can pull information from all tables on the players profile.

# Implementation
Scrapping was done using the Beautiful Soup and Request libraries.
Data is processed using pandas and exported using either CSV or XLSX.

# Imports 
Libraries needed: 
  Beautiful Soup
  Requests
  XlsxWriter
  Pandas

pip install XlsxWriter
pip install beautifulsoup4
pip install numpy<2
pip install requests

# Usage
Running main.py prompts the user through typical flow of obtaining player data.
The flow is as follows:
  - What information the user wants (Season Averages)
  - What metrics the user wants (multiple can be chosen)
  - What file name the data will be exported to
  - Whether the user wants to continue

# Data
If the user selects only one stat to export the data will be exported as CSV.
If the user selects multiple stats to export the data will be exported as XLSX.
The table structure will follow the tables as shown on basketballreference.com as 
closely as possible. Exceptions occur with merged cells which are excluded from 
the tables.

# Understanding the classes
# Player
The Player class serves to get general information about a player which currently 
implements finding the url of the player

# Player Season
The PlayerSeason class serves to pull season by season data from the players main
page using Beautiful Soup and Request libraries.

For certain tables the request response does not give the active HTML of the table
but instead commented out placeholder code in place of the HTML that is seen when
visiting the website. I have converted the comment into HTML and processed it 
but there are no guarantees that this provides the most up to data statistics 
if this is the placeholder code and this code is not updated. From an eye test
the data looks accurate.

