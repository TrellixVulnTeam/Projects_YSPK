#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

if __name__ == "__main__":
    countryCodesStructuredFilePath = "iso-3166-alpha-2-country-codes-structered.json"
    databaseCountiesFilePath = "databaseCountries.json"
    errorLogJsonFilePath = "keyErrorCheckResult.json"
    countryCodesStructuredData = json.load(open(countryCodesStructuredFilePath, "r", encoding = "utf8"))
    databaseCountiesFilePathData = json.load(open( databaseCountiesFilePath, "r", encoding = "utf8"))
    errorCounterArray = list()
    
    for key in databaseCountiesFilePathData:
        try:
            countryCodesStructuredData[key]
        except KeyError:
            print("Error with key", key)
            errorCounterArray.append(key)
            
    with open(errorLogJsonFilePath, "w", encoding = "utf8") as outfile:
        json.dump(errorCounterArray, outfile)