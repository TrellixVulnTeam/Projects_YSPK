#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import urllib2
"""
General Purpose: Crawls elasticsearch data in a specific 
timeframe and saves every document in a jsoon file

Resultant Folder structure:
    data:
        for each year a folder:
            for every month a folder:
                for every day a folder:
                    json files from that day
"""
import json
import os
import requests
from calendar import monthrange

# make folder data if not existing
def initRootDir():
    folder = "data"
    if not os.path.isdir(folder):
        os.mkdir(folder)

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
    "size" : 10000,
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

# Function for writing every recieved document to a json file on Disk 
def writeDataToDisc(folder, recievedData):
    for i in range(len(recievedData["hits"]["hits"])):
        fileName = str(i) + "-" + recievedData["hits"]["hits"][0]["_source"]["created_at"] + ".json"
        print("Saving", str(i) + ".", "Record", "to", fileName)
        with open(folder + fileName, 'w') as outfile:
            json.dump(recievedData["hits"]["hits"][i]["_source"], outfile)
            
            
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
    
    rootDir = "data"
    
    initRootDir()
    
    # A Mapper for a month number to a month name for later use as folder name 
    monthNames = {"01" : "January", "02" : "February", "03" : "March", "04" : "April", "05" : "May", "06" : "June", "07" : "July", "08" : "August", "09" : "September", "10" : "October", "11" : "November", "12" : "December"}
    
    configData = json.load(open("config.json"))
    host = configData["host"]
    user = configData["user"]
    password = configData["password"]
    
    url = buildURL(host, user, password)

    """
    main driver part for crawling all data from example 2020, 2019 etc
    """
    for year in years:
        folder = rootDir + "/" + year
        os.mkdir(folder)
        for month in range(len(months)):    
            folder = rootDir + "/" + year + "/" + monthNames[months[month]]
            os.mkdir(folder)
            for day in getDaysOfMonthAsList(int(months[month]), int("2020")):
                folder = rootDir + "/" + year + "/" + monthNames[months[month]] + "/Day " + day
                os.mkdir(folder)
                print("Get Records from", year + "/" + months[month] + "/" + day + "...")
                print("------------------------------")
                print("")
                for h in range(len(hours)):
                    for m in range(len(minutes)):
                        date = "2020-" + months[month] + "-" + day
                        data = createJsonStructure(date, hours[h], hours[h], minutes[m], minutes[m+1] if m < len(minutes)-1 else minutes[0])
                        sender = {"source": json.dumps(data), "source_content_type": "application/json"}
                        recievedData = requests.get(url, params=sender).json()
                        writeDataToDisc(folder + "/", recievedData)
                print("")
                print("------------------------------")
                print("")
            
    

    