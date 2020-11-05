#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Purpose: a class containing all weighing schemes for the
analysis of the given data
"""
import filter as fs

class WeighingSchemes:
    # init function for setting globals 
    def __init__(self, connection, tableName):
        self.databaseConnection = connection
        self.tableName = tableName
        self.filterObject = fs.Filter()
    
    """
    this function contains a Frequency Analysis of the Hashtags in 
    the given data for one particular date which will be given as 
    parameter and input from the user, the result will be a dictionary
    containing the hashtags as key and some number as value
    example: {#Merkel : 10, #welt : 1} etc
    """
    def frequencyAnalysisWithParticularizedDate(self, date, year):
        result = dict()
        query = "SELECT DISTINCT text FROM " + self.tableName
        query += " WHERE MATCH(created_at) AGAINST('+\"" + date + "\" +" +  year + "'"
        query += " IN BOOLEAN MODE);"
        resultOfQuery = self.databaseConnection.executeQuery(query)
        for i in range(len(resultOfQuery)):
            for item in self.filterObject.filterString(resultOfQuery[i][0]):
                if item in result.keys():
                    result[item] += 1
                else: 
                    result[item] = 1
        return result
    
    """
    this function contains a Frequency Analysis of the Hashtags in 
    the given data for one particular date summed up to one week  
    starting from the date parameter which will be given as 
    parameter and input from the user, the result will be a dictionary
    containing the hashtags as key and some number as value
    example: {#Merkel : 10, #welt : 1} etc
    """
    def frequencyAnalysisWithParticularizedDateSummedUpToWeek(self, date, year):
        result = dict()
        dayAsString = str(date.split(" ")[1])
        for i in range(8):  
            dayAsNumber = int(dayAsString) + i
            print(dayAsNumber)
            day = " 0" + str(dayAsNumber) if dayAsNumber < 10 else " " + str(dayAsNumber)
            newDate = date.split(" ")[0] +  day
            resultOfQuery = self.frequencyAnalysisWithParticularizedDate(newDate, year)
            for item in resultOfQuery:
                if item in result.keys():
                    result[item] += resultOfQuery[item]
                else: 
                    result[item] = resultOfQuery[item]
        return result
    
    """
    this function contains a Frequency Analysis of the Hashtags in 
    the given data for one particular month which will be given as 
    parameter and input from the user, the result will be a dictionary
    containing the hashtags as key and some number as value
    example: {#Merkel : 10, #welt : 1} etc
    """
    def frequencyAnalysisWithParticularizedDateSummedUpToMonth(self, month, year):
        result = dict()
        query = "SELECT DISTINCT text FROM " + self.tableName
        query += " WHERE MATCH(created_at) AGAINST('+" +  month + " +" +  year + "'"
        query += " IN BOOLEAN MODE);"
        resultOfQuery = self.databaseConnection.executeQuery(query)
        for i in range(len(resultOfQuery)):
            for item in self.filterObject.filterString(resultOfQuery[i][0]):
                if item in result.keys():
                    result[item] += 1
                else: 
                    result[item] = 1
        return result
    
    """
    this function contains the analysis of the data by the a counter paramter
    sorted from most post to least post in the database
    the result contains a list of lists which contains each hashtag of the specific
    post, because of the sorting in SQL statement the result is also sorted 
    according to that
    """
    def analysisOfDataFRomASpecificDateWithTwitterCounter(self, date, counter, sorting, year):
        result = dict()
        query = "SELECT DISTINCT text, " + counter + " FROM " + self.tableName
        query += " WHERE MATCH(created_at) AGAINST('+\"" + date + "\" +" +  year + "'"
        query += " IN BOOLEAN MODE)"
        query += " ORDER by " + counter + " " + sorting + ";"
        resultOfQuery = self.databaseConnection.executeQuery(query)
        for i in range(len(resultOfQuery)):
            key = ', '.join(map(str, self.filterObject.filterString(resultOfQuery[i][0])))
            result["[" + key + "]"] = int(resultOfQuery[i][1])
        return result
        
    
    """
    this function containts the frequency of hashtags in a specific date
    on workdays the result will be dictionary containing the hashtags as key
    and the freuquency of the key as value
    example: {#witze : 10, #arbeit: 100}
    """
    def analysisOfWorkdaysForASpecificDate(self, date, year):
        result = dict()
        query = "SELECT DISTINCT text FROM " 
        query += self.tableName + " WHERE MATCH(created_at) AGAINST('+\""
        query += date + "\" +" + year + " -Sun -Sat' IN BOOLEAN MODE);"
        resultOfQuery = self.databaseConnection.executeQuery(query)
        for i in range(len(resultOfQuery)):
            for item in self.filterObject.filterString(resultOfQuery[i][0]):
                if item in result.keys():
                    result[item] += 1
                else: 
                    result[item] = 1
        return result
    
    """
    this function containts the frequency of hashtags in a specific date
    on weekend the result will be dictionary containing the hashtags as key
    and the freuquency of the key as value
    example: {#witze : 10, #bier: 100}
    """
    def analysisOfWeekendaysForASpecificDate(self, date, year):
        result = dict()
        query = "SELECT DISTINCT text FROM " + self.tableName
        query += " WHERE MATCH(created_at) AGAINST('+\""
        query += date + "\" +" + year + " -Mon -Tue -Wed -Thu -Fri'"
        query += " IN BOOLEAN MODE);"
        resultOfQuery = self.databaseConnection.executeQuery(query)
        for i in range(len(resultOfQuery)):
            for item in self.filterObject.filterString(resultOfQuery[i][0]):
                if item in result.keys():
                    result[item] += 1
                else: 
                    result[item] = 1
        return result
    
    """
    this function containts the hashtags in a specific date
    and the differences hashtags which only where posted on workdays and which
    ones where only posted on weekend and returned as a list with two sublists
    the first = hashtags only on workdays
    the second = hashtags only on weekends
    """    
    def analysisOfDifferenceInHashtagsWorkdayAndWeekends(self, date, year):
        resultWorkdays = self.analysisOfWorkdaysForASpecificDate(date, year)
        resultWeekenddays = self.analysisOfWeekendaysForASpecificDate(date, year)
        differenceWorkdays = set(resultWorkdays.keys()).difference(set(resultWeekenddays.keys()))
        differenceWeekend = set(resultWeekenddays.keys()).difference(set(resultWorkdays.keys()))
        resultA = list(differenceWorkdays)
        resultB = list(differenceWeekend)
        return resultA, resultB
    
    """
    this function contains the frequency of hashtags used by every country on a
    specific date, the result will be  dictionary containig several dictionaries
    the first level will contain the language/country as key the value is a 
    dictionary containing the hashtags as key andthe frequency as value
    example: {"de" : {#witze : 10}, "fr" : {#paris : 10}}
    """
    def analysisOfHashtagsForEachCountryOnaSpecificDateWithFrequency(self, date, year):
        query = "SELECT DISTINCT text, lang FROM " + self.tableName
        query += " WHERE MATCH(created_at) AGAINST('+\"" + date + "\" +" +  year + "'"
        query += " IN BOOLEAN MODE);"
        queryLangKeys = "SELECT DISTINCT lang FROM " + self.tableName
        queryLangKeys += " WHERE MATCH(created_at) AGAINST('+\"" + date + "\" +" +  year + "'"
        queryLangKeys += " IN BOOLEAN MODE);"
        resultQuery = self.databaseConnection.executeQuery(query)
        resultLangKeys = self.databaseConnection.executeQuery(queryLangKeys)
        langTextPairs ={ key : [] for key in [resultLangKeys[i][0] for i in range(len(resultLangKeys))]}
        for i in range(len(resultQuery)):
            langTextPairs[resultQuery[i][1]].append(self.filterObject.filterString(resultQuery[i][0]))
        for key in langTextPairs.keys():
            temp = dict()
            for i in range(len(langTextPairs[key])):
                for item in langTextPairs[key][i]:
                    if item in temp.keys():
                        temp[item] += 1
                    else:
                        temp[item] = 1
                temp = self.filterObject.sortDictionary(temp, True)
            langTextPairs[key] = dict(temp) 
        return langTextPairs
    
    
    """
    this function contains the hashtags witheld by a specific country on a
    specific date, the result will be  dictionary containig a list
    the first level will contain the language/country as key the value is a 
    list containing the hashtags 
    example: {"de" : [#rechts, #abendland], "fr" : {#pariserterror, #negro}
    """
    def analysisOfPostsWithHashtagsWithheldInCountriesOnASpecificDate(self, date, year):
        query = "SELECT DISTINCT text, withheld_in_countries FROM " + self.tableName
        query += " WHERE withheld_in_countries IS NOT NULL AND "
        query += " MATCH(created_at) AGAINST('+\"" + date + "\" +" +  year + "'"
        query += " IN BOOLEAN MODE);"
        queryWithHeld = "SELECT DISTINCT withheld_in_countries FROM " + self.tableName
        queryWithHeld += " WHERE withheld_in_countries IS NOT NULL AND "
        queryWithHeld += " MATCH(created_at) AGAINST('+\"" + date + "\" +" +  year + "'"
        queryWithHeld += " IN BOOLEAN MODE);"
        resultQuery = self.databaseConnection.executeQuery(query)
        resultWithHeld = self.databaseConnection.executeQuery(queryWithHeld)
        withHeldHashTags = { key : [] for key in [resultWithHeld[i][0] for i in range(len(resultWithHeld))]}
        for i in range(len(resultQuery)):
            withHeldHashTags[resultQuery[i][1]].append(self.filterObject.filterString(resultQuery[i][0]))
        for key in withHeldHashTags.keys():
            temp = list()
            for i in range(len(withHeldHashTags[key])):
                for item in withHeldHashTags[key][i]:
                    temp.append(item)
            withHeldHashTags[key] = list(temp)
        return withHeldHashTags
    
    """
    this function contains the hashtags posted on either at day times or at night
    tmes for specific date, the result will be  two list containing the hashtags for the day and
    night
    example: [#sommer, #sonne, #tag] [#party, #rockNroll, #nacht]
    """        
    def analysisOfHashtagsDayNightCycleWithSpecificDate(self, date, year):
        day, night = list(), list()
        nightMathes = list()
        query = "SELECT DISTINCT text, created_at FROM " + self.tableName
        query += " WHERE MATCH(created_at) AGAINST('+\"" + date + "\" +" +  year + "'"
        query += " IN BOOLEAN MODE);"
        resultQuery = self.databaseConnection.executeQuery(query)
        for i in range(24):
            if i < 6 or i > 19:
                nightMathes.append(date + " 0" + str(i) if i < 10 else date + " " + str(i))
        for i in range(len(resultQuery)):
            if any(x in resultQuery[i][1] for x in nightMathes):
                night.append(self.filterObject.filterString(resultQuery[i][0]))
            else:
                day.append(self.filterObject.filterString(resultQuery[i][0]))
        day = set([item for sublist in day for item in sublist])
        night = set([item for sublist in night for item in sublist])
        resultDay = list(day.difference(night))
        resultNight = list(night.difference(day))
        return resultDay, resultNight
        
    """
    this function contains the difference in hashtags for two specific dates
    the result will be a list of hashtags
    example: [#sonne, #bier, #nacht]
    """    
    def findNewHashtagsFomTwoDates(self, dateA, dateB, yearA, yearB):
        queryA = "SELECT DISTINCT text FROM " + self.tableName
        queryA += " WHERE MATCH(created_at) AGAINST('+\"" + dateA + "\" +" +  yearA + "'"
        queryA += " IN BOOLEAN MODE);"
        queryB = "SELECT DISTINCT text FROM " + self.tableName
        queryB += " WHERE MATCH(created_at) AGAINST('+\"" + dateB + "\" +" +  yearB + "'"
        queryB += " IN BOOLEAN MODE);"
        resultOfQueryA = self.databaseConnection.executeQuery(queryA)
        resultOfQueryB = self.databaseConnection.executeQuery(queryB)
        resultOfQueryAFiltered, resultOfQueryBFiltered  = list(), list()
        for i in range(len(resultOfQueryA)):
            for item in self.filterObject.filterString(resultOfQueryA[i][0]):
                 resultOfQueryAFiltered.append(item)
        for i in range(len(resultOfQueryB)):
            for item in self.filterObject.filterString(resultOfQueryB[i][0]):
                 resultOfQueryBFiltered.append(item)
        differenceQueryA = set(resultOfQueryAFiltered).difference(set(resultOfQueryBFiltered))
        differenceQueryB = set(resultOfQueryBFiltered).difference(set(resultOfQueryAFiltered))
        resultA = list(differenceQueryA)
        resultB = list(differenceQueryB)
        return resultA, resultB
    
        