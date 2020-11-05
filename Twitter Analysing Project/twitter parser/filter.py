#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Purpose: a class for filterimg all #Hashtags in a string and put 
them in a list and return the list and for type conversions, sorting and organization
of tasks
"""
import re
import time
import datetime

class Filter:
    # init function
    def __init__(self):
        self.stringToFilter = None
    
    # function for filtering the hashtags of a string    
    def filterString(self, string):
        self.stringToFilter = string
        realResult = list()
        result = re.split("\s", self.stringToFilter)
        for s in result:
            if "#" in s:
                if s.count("#") > 1:
                    for sp in s.split("#"):
                        if sp != '': realResult.append("#" + sp)
                elif re.search("^#", s) != None:
                    realResult.append(re.search("^#", s).string)
        return realResult
    
    """
    function for sorting a dictionary by its values in ascendind or descending
    order
    """
    def sortDictionary(self, dictionary, reversing = False):
        return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=reversing)}
    
    # a function for converting the date so it can be usable in the sql database
    def convertInputDateToUsableDate(self, string, inputFormat, outputFormat):
        dateObject = datetime.datetime.strptime(string, inputFormat)
        return dateObject.strftime(outputFormat)
    
    def getWeekDaysOfAWeekForASpecificDate(self, date, year):
        useableDateParametersAsInt = [int(s) for s in 
                                      self.convertInputDateToUsableDate(date + " " + year, 
                                                                   "%b %d %Y",
                                                                   "%d %m %Y").split(" ")]
        weekNumber  = datetime.date(useableDateParametersAsInt[2], 
                                    useableDateParametersAsInt[1],
                                    useableDateParametersAsInt[0]).isocalendar()[1] - 1 
        startdate = time.asctime(time.strptime(str(year) + ' %d 1' % weekNumber, 
                                               '%Y %W %w')) 
        startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y') 
        dates = [startdate.strftime('%d-%b-%Y')] 
        for i in range(1, 7): 
            day = startdate + datetime.timedelta(days=i)
            dates.append(day.strftime('%d-%b-%Y'))
        return dates
    
    