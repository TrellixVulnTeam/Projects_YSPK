#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Purpose: Counts how manay files have a diffent structure of keys
in json file as the first json file 
"""
import json
import os
from calendar import monthrange

# Get the days of a specific month in a specific year as List
def getDaysOfMonthAsList(month, year):
    return ["0" + str(i) if i < 10 else str(i) for i in range(1, monthrange(year, month)[1]+1)]

# a fucntion to add 2 arrays save the rsult in a third
def addArrays(arrayA, arrayB):
    array = [ 0 for i in range(len(arrayA))]
    for i in range(len(arrayA)):
        array [i] = arrayA[i] + arrayB[i]
    return array

# a function for checking two json files fo the same key structure
def checkFileStructure(fileA, fileB):
    dataA, dataB = json.load(open(fileA)), json.load(open(fileB))
    return True if list(dataA.keys()) == list(dataB.keys()) else False

# a function to iterate over all files in a specific folder
def counterOfAllStatsPerDay(folder, compareToFile):
    counter = [0, 0, 0]
    files = next(os.walk(folder))[2]
    for fileAIndex in range(len(files)):
        print("Compare", compareToFile, "and", files[fileAIndex])
        fileA = folder + "/" + files[fileAIndex]
        counterIndex = 0 if checkFileStructure(compareToFile, fileA) else 1
        counter[counterIndex] += 1
        counter[2] += 1
        print("Current Result:", counter)
    return counter

"""
a function to iterate over all files in a specific folder with folder in it 
named after months
"""    
def countAllStatsPerMonth(folder):
    counter = [0, 0, 0]
    monthNames = ["Januray", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", 
                   "December"]
    months = ["0" + str(i) if i < 10 else str(i) for i in range(1, 13)]
    compareToFile = folder + "/Januray/Day 01/" + sorted(next(os.walk(folder + "/Januray/Day 01"))[2])[0]
    for monthIndex in range(len(monthNames)):
        for dayName in getDaysOfMonthAsList(int(months[monthIndex]), int("2020")):
            folderNew = folder + "/" + monthNames[monthIndex] + "/" + "Day " + dayName
            print("Checking Folder", folderNew)
            print("---------------------------")
            counterNew = counterOfAllStatsPerDay(folderNew,  compareToFile) if os.path.isdir(folderNew) else [0, 0, 0]
            counter = addArrays(counter, counterNew)
            print("Current summed Result:", counter)
            print("")
            print("---------------------------")
            print("")
    return counter

# a function for displaying the rsult of the test
def displayAllstats(counter):
    print("")
    print("---------------------------")
    print("Count of equal Structure Files:", counter[0])
    print("Count of not equal Structure Files:", counter[1])
    print("Total Files:", counter[2])

# main function of program
if __name__ == "__main__":    
    folder = "twitterData/2020"
    resultOfCount =[0, 0, 0]
    resultOfCount = addArrays(resultOfCount, countAllStatsPerMonth(folder))
    displayAllstats(resultOfCount)



        
        
        
        
    


