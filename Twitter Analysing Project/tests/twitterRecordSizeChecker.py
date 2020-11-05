#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Purpose: checks if crawled elasticsearch data is under 
10.000 of total hits if not query must be made more exact
"""
import json
import requests
from calendar import monthrange

# Get the days of a specific month in a specific year as List
def getDaysOfMonthAsList(month, year):
    return ["0" + str(i) if i < 10 else str(i) for i in range(1, monthrange(year, month)[1]+1)]

# build search URL to coonect to server later
def buildURL(adress, user, passwordFile):
    url = "https://" + user + ":"
    url += open(passwordFile, "r").readline() + "@"
    url += adress
    return url

"""
Bulid the elasticsearch Query with a start date and end date in which the data 
is crawled
"""
def createJsonStructure(date, startTimeh, endTimeh, startTimem, endTimem):
    data = { 
    "query": { 
      "bool": {
        "must": [],    
        "filter": [
            { "match_all": {} },      
            { "range":
                { "created_at": {
                    "format": "strict_date_optional_time",
                    "gte": date + "T" + startTimeh + ":" + startTimem + ":00.000Z",
                    "lte": date + "T" + endTimeh + ":" + endTimem + ":00.000Z"}        
                     }      
                  }    
                ],    
            "should": [],    
            "must_not": []  
        }
    }}
    return data

#Function for checking if total hits of each query is under 10.000
def checkTotalHits(hitsNumber, logFile):
        if hitsNumber < 10000:
            print("CHECKED OK:", hitsNumber)
            logFile.write("CHECKED OK: " + str(hitsNumber) + "\n")
            return True
        else:
            print("ERROR:", hitsNumber)
            logFile.write("ERROR: " + str(hitsNumber) + "\n")
            return False

#Function for writing a beginning string to file
def writeStartOfCkeckToFile(string, logFile):
    logFile.write(string)
    logFile.write("------------------------------\n")
    logFile.write(" \n")

#Function for writing a ending string to file 
def writeEndOfCkeckToFile(logFile):
    logFile.write(" \n")
    logFile.write("------------------------------\n")
    logFile.write(" \n")
    

# main function of program
if __name__ == "__main__":        
    """
    define hours of a day as array of strings with appearance 00, 01, ... , 10 ...
    define minutes of a houer as array of strings with appearance 00, 01, ... , 10 ...
    define months of a year as array of strings with appearance 00, 01, ... , 10 ...
    define years as array of strings
    """
    hours = ["0" + str(i) if i < 10 else str(i) for i in range(24)]
    months = ["0" + str(i) if i < 10 else str(i) for i in range(1, 13)]
    minutes = ["0" + str(i) if i < 10 else str(i) for i in range(0, 60, 10)]
    years = ["2020"]
    
    # A Mapper for a month number to a month name for later use as folder name 
    monthNames = {"01" : "January", "02" : "February", "03" : "March", "04" : "April", "05" : "May", "06" : "June", "07" : "July", "08" : "August", "09" : "September", "10" : "October", "11" : "November", "12" : "December"} 
    
    url = buildURL("elastic-dbs.ifi.uni-heidelberg.de/twitter_pipeline/_search?pretty=true", "pwiedemann", "secrets.txt")
    logFilePath = "testLogs/recordSizeCheckerLog.txt"

    """
    main driver part for checking all data from example 2020, 2019 etc
    """
    with open(logFilePath, 'a') as outfile:
        for year in years:
            for month in range(len(months)):    
                for day in getDaysOfMonthAsList(int(months[month]), int("2020")):
                    print("Get Records from", year + "/" + months[month] + "/" + day + "...")
                    print("------------------------------")
                    print("")
                    writeStartOfCkeckToFile("Get Records from " + year + "/" + months[month] + "/" + day + "...", outfile)
                    for h in range(len(hours)):
                        for m in range(len(minutes)):
                            date = "2020-" + months[month] + "-" + day
                            data = createJsonStructure(date, hours[h], hours[h], minutes[m], minutes[m+1] if m < len(minutes)-1 else minutes[0])
                            sender = {"source": json.dumps(data), "source_content_type": "application/json"}
                            recievedData = requests.get(url, params=sender).json()
                            if not checkTotalHits(recievedData["hits"]["total"]["value"], outfile):
                                print("ERROR Records > 10000 | stopping Record Size Checker")
                    print("")
                    print("------------------------------")
                    print("")
                    writeEndOfCkeckToFile(outfile)


