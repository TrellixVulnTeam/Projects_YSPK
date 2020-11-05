#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Purpose: a class for filterimg all #Hashtags in a string and put 
them in a list and return the list and for type conversions, sorting and organization
of tasks
"""
import re
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
    
    