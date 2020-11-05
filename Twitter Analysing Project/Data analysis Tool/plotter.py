#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import weighingSchemes as ws
import matplotlib.pyplot as plt
from calendar import monthrange
from datetime import datetime
import json
import filter as fs

class Plotter:
    def __init__(self, connection, tableName):
        self.schemesObject = ws.WeighingSchemes(connection, tableName)
        self.filterObject = fs.Filter()
        self.countryCodesMapper = json.load(
            open("countryCodesJsons/iso-3166-alpha-2-country-codes-structered.json"
                 , "r", encoding = "utf8"))
    
    def getShortMonthAsNumberMapper(self):
        mapper = {"Jan" : 1, "Feb" : 2, "Mar" : 3, "Apr": 4, "May" : 5}
        return mapper
        
    #function for getting the number of a month    
    def getDaysOfMonthAsList(self, month, year):
        return ["0" + str(i) if i < 10 else str(i) for i in range(1, monthrange(year, month)[1]+1)]
    
    def makeDirectoryIfNotExists(self, dirName):
        if not os.path.isdir(dirName):
            os.mkdir(dirName)
            print("Created Directory", dirName)
    
    def plotDiagram(self, xAxis, yAxis, labels, fileName, options = 
                    [(15, 8), 100, 70]):
        plt.switch_backend('Agg')
        plt.figure(figsize = options[0], dpi = options[1])
        plt.plot(xAxis, yAxis, "ro")
        plt.title(labels[0])
        plt.xlabel(labels[1])
        plt.ylabel(labels[2])
        plt.xticks(rotation = options[2])
        plt.savefig(fileName + ".png", dpi = options[1])
        print("Saved", fileName)
        
    def plotFrequencyAnalysisWithParticularizedDateForAMonth(self, month, year):
        result = [[], []]
        labels = ["Most used Hashtag per Day in " 
                  + month + " " + year, "Day", "Hashtags"]
        daysAsString = self.getDaysOfMonthAsList(self.getShortMonthAsNumberMapper()[month], int(year))
        for dayString in daysAsString:
            result[0].append(dayString)
            date = month + " " + dayString
            dictResult = self.schemesObject.frequencyAnalysisWithParticularizedDate(date, year)
            tempResult = self.filterObject.sortDictionary(dictResult, reversing = True)
            result[1].append(list(tempResult.keys())[0] if list(tempResult.keys()) else "No Hashtags posted")
        return result, labels
    
    def plotFrequencyAnalysisWithParticularizedDateSummedUpToMonthForEachMonth(self, year):
        result = [[], []]
        labels = ["Most used Hashtag per Month in " + year, 
                  "Month", "Hashtags"]
        month = ["Jan", "Feb", "Mar", "Apr", "May"]
        for m in month:
            result[0].append(m)
            dictResult = self.schemesObject.frequencyAnalysisWithParticularizedDateSummedUpToMonth(m, year)
            tempResult = self.filterObject.sortDictionary(dictResult, reversing = True)
            result[1].append(list(tempResult.keys())[0] if list(tempResult.keys()) else "No Hashtags posted")
        return result, labels
    
    def plotAnalysisOfWorkdaysForASpecificDateEachMonth(self, year):
        result = [[], []]
        labels = ["Most used Hashtag posted on Workdays per Month in " + year, 
                  "Month", "Hashtags"]
        month = ["Jan", "Feb", "Mar", "Apr", "May"]
        for m in month:
            result[0].append(m)
            dictResult = self.schemesObject.analysisOfWorkdaysForASpecificDate(m, year)
            tempResult = self.filterObject.sortDictionary(dictResult, reversing = True)
            result[1].append(list(tempResult.keys())[0] if list(tempResult.keys()) else "No Hashtags posted")
        return result, labels
    
    def plotAnalysisOfWeekendaysForASpecificDateEachMonth(self, year):
        result = [[], []]
        labels = ["Most used Hashtag posted on Weekend per Month in " + year, 
                  "Month", "Hashtags"]
        month = ["Jan", "Feb", "Mar", "Apr", "May"]
        for m in month:
            result[0].append(m)
            dictResult = self.schemesObject.analysisOfWeekendaysForASpecificDate(m, year)
            tempResult = self.filterObject.sortDictionary(dictResult, reversing = True)
            result[1].append(list(tempResult.keys())[0] if list(tempResult.keys()) else "No Hashtags posted")
        return result, labels
    
    def plotAanalysisOfHashtagsForEachCountryOnaSpecificDateWithFrequency(self, month, year):
        result = [[], []]
        labels = ["Most used Hashtags sorted by Country in " 
                  + month + " " + year, "Country", "Hashtags"]
        dictResult = self.schemesObject.analysisOfHashtagsForEachCountryOnaSpecificDateWithFrequency(month, year)
        for key in dictResult.keys():
            result[0].append(self.countryCodesMapper[key.replace("\"", "")])
            result[1].append(list(dictResult[key].keys())[0] if list(dictResult[key].keys()) else "No Hashtags posted")
        return result, labels
    
    def mainPlotAll(self, year):
        month = ["Jan", "Feb", "Mar", "Apr", "May"]
        dirPath = "Plots/" + datetime.today().strftime('%d-%m-%Y') 
        self.makeDirectoryIfNotExists("Plots")
        self.makeDirectoryIfNotExists(dirPath)
        print("")
        print("plotFrequencyAnalysisWithParticularizedDateForAMonth")
        print("----------------------------------------------")
        for m in month:
            print("Getting Results for ", m, year)
            print("----")
            result, labels = self.plotFrequencyAnalysisWithParticularizedDateForAMonth(m, year)
            fileName = dirPath + "/" + labels[0]
            self.plotDiagram(result[0], result[1], labels, fileName)
            print("----")
        print("----------------------------------------------")
        print("")
        print("plotFrequencyAnalysisWithParticularizedDateSummedUpToMonthForEachMonth")
        print("----------------------------------------------")
        result, labels = self.plotFrequencyAnalysisWithParticularizedDateSummedUpToMonthForEachMonth(year)
        fileName = dirPath + "/" + labels[0]
        self.plotDiagram(result[0], result[1], labels, fileName)
        print("----------------------------------------------")
        print("")
        print("plotAnalysisOfWorkdaysForASpecificDateEachMonth")
        print("----------------------------------------------")
        result, labels = self.plotAnalysisOfWorkdaysForASpecificDateEachMonth(year)
        fileName = dirPath + "/" + labels[0]
        self.plotDiagram(result[0], result[1], labels, fileName)
        print("----------------------------------------------")
        print("")
        print("plotAnalysisOfWeekendaysForASpecificDateEachMonth")
        print("----------------------------------------------")
        result, labels = self.plotAnalysisOfWeekendaysForASpecificDateEachMonth(year)
        fileName = dirPath + "/" + labels[0]
        self.plotDiagram(result[0], result[1], labels, fileName)
        print("----------------------------------------------")
        print("")
        print("plotAanalysisOfHashtagsForEachCountryOnaSpecificDateWithFrequency")
        print("----------------------------------------------")
        for m in month:
            print("Getting Results for ", m, year)
            print("----")
            result, labels = self.plotAanalysisOfHashtagsForEachCountryOnaSpecificDateWithFrequency(m, year)
            fileName = dirPath + "/" + labels[0]
            self.plotDiagram(result[0], result[1], labels, fileName, 
                             options = [(15, 15), 100, 90])
            print("----")
        print("----------------------------------------------")