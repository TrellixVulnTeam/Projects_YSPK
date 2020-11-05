#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Purpose: a general porter from elastic search data to a 
mariaDB/mySQL database

creates table from a build structure from the jsons files
inserts all data from the json file into the database

Folder structure:
    data:
        for each year a folder:
            for every month a folder:
                for every day a folder:
                    json files from that day
"""
import os
import json
import mysql.connector as mc
from calendar import monthrange

#  function for getting the password rom a file
def getPasswordForDatabaseConnection(passwordFile):
    return open(passwordFile, "r").readline() 

# function for connecting to the database
def createConnectionToMySQLDatabase(address, user, password, database):
    return mc.connect (host = address, user = user,
                       passwd = password, db = database)

#function for closing the connection
def closeConnectionToMySQLDatabase(connection):
    connection.close()

#function for getting the number of a month    
def getDaysOfMonthAsList(month, year):
    return ["0" + str(i) if i < 10 else str(i) for i in range(1, monthrange(year, month)[1]+1)]

#function for getting the name of a month       
def getMonthFolderNameList():
    monthNames = ["Januray", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", 
                   "December"]
    return monthNames

#function for getting the SQL Datatype in realtion to the Python Datatype
def pythonTypeToSQLType(key):
    mapper = {type(int()).__name__ : "BIGINT", type(bool()).__name__ : "BOOL",
              type(str()).__name__ : "VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci",
              type(None).__name__ : "VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci",
              type(dict()).__name__ : "LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci", 
              type(list()).__name__ : "VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"}
    return mapper[type(key).__name__]

"""
a function for adding the new keys from 2 dicts
used for building the tempalte for the SQL table
"""
def checkIfKeyOrValueIsNew(oldDict, newDict):
    result = dict(oldDict)
    for key in newDict.keys():
        if (not key in list(oldDict.keys())) or (oldDict[key] == None):
            if (not key in list(oldDict.keys())):
                print("Found New Key to add:", key)
            result[key] = newDict[key]
    return result

"""
a function to collect all new keys
used for building the tempalte for the SQL table
"""
def getKeyValuePairsFromFiles(folder, mapper):
    result = dict(mapper)
    files = next(os.walk(folder))[2]
    for fileIndex in range(len(files)):
        loadFile = folder + "/" + files[fileIndex]
        tempData = json.load(open(loadFile))
        result = checkIfKeyOrValueIsNew(result, tempData)
    return result

#used for saving the sql table template
def saveTableTemplateToBuildFolder(template): 
    saveFolder, fileName = "build", "tableTemplateFromData.json" 
    filePath = saveFolder + "/" + fileName
    if not os.path.isdir(saveFolder):
        os.mkdir(saveFolder)
    with open(filePath, "w") as file:
        json.dump(template, file)

#used for building the tempalte for the SQL table    
def createTableTemplateFromData(folder):
    monthNames = getMonthFolderNameList()
    months = ["0" + str(i) if i < 10 else str(i) for i in range(1, 13)]
    years =  ["2020"]
    result = dict()
    print("Creating Table Template")
    print("-----------------------")
    print("")
    for year in years:
        for monthIndex in range(len(monthNames)):
            for dayName in getDaysOfMonthAsList(int(months[monthIndex]), int("2020")):
                folderNew = folder + "/" + year + "/" + monthNames[monthIndex] + "/" + "Day " + dayName
                if os.path.isdir(folderNew):
                    result =  getKeyValuePairsFromFiles(folderNew, result)
    saveTableTemplateToBuildFolder(result)
    print("")
    print("-----------------------")
    print("Finished createing and saving Template")

# function for creating the CREATE TABLE string from a jsonfile
def buildTableStatement(tablename, jsonFilePath):
    query = "CREATE TABLE IF NOT EXISTS " + tablename + " (" + tablename+ "_ID INTEGER AUTO_INCREMENT PRIMARY KEY, "
    jsonData = json.load(open(jsonFilePath))
    for key in jsonData.keys():
        query += key + " " + pythonTypeToSQLType(jsonData[key])
        if key != list(jsonData.keys())[-1]: query += ", "
    query += ") CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    return query

# function for creating the INSERT INTO string from a jsonfile
def bulidInsertStatement(tablename, jsonFilePath):
    query = "INSERT INTO " + tablename + "("
    jsonData = json.load(open(jsonFilePath))
    for key in jsonData.keys():
        query += key
        if key != list(jsonData.keys())[-1]: query += ", "
    query += ") VALUES ("
    for key in jsonData.keys():
        if jsonData[key] == None:
            query += "NULL"
        elif type(jsonData[key]) == type(dict()):
            query += "'" + json.dumps(jsonData[key], ensure_ascii=False).replace("'", "''") + "'"
        elif type(jsonData[key]) == type(list()):
            query += "'" + ';'.join(map(str, jsonData[key])).replace("'", "''") + "'"
        elif not type(jsonData[key]) == type(str()):
            query += str(jsonData[key]) 
        else:
            query += "'" + json.dumps(jsonData[key], ensure_ascii=False).replace("'", "''") + "'"
        if key != list(jsonData.keys())[-1]: query += ", "
    query += ");"
    return query

def createTables(connection, tableNames, jsonFilePathes):
    cursor = connection.cursor()
    for i in range(len(tableNames)):
        tableQuery = buildTableStatement(tableNames[i], jsonFilePathes[i])
        cursor.execute(tableQuery)
        connection.commit()
    cursor.close()
     
def executeInsertQuery(connection, tableName, jsonFilePath):
     cursor = connection.cursor()
     insertQuery = bulidInsertStatement(tableName, jsonFilePath)
     cursor.execute(insertQuery)
     connection.commit()
     cursor.close()

"""
inserts all json documents in a folder into the SQL database
"""     
def insertEveryJsonDocumentOfAFolderInDatabase(connection, folder, tableName):
    files = sorted(next(os.walk(folder))[2])
    for file in files:
        filePath = folder + "/" + file
        print(filePath)
        executeInsertQuery(connection, tableName, filePath)

"""
executes the inserion of al json files
"""     
def executeInsersionOfAllJsonInDatabase(connection, folder, tableName):
    monthNames = getMonthFolderNameList()
    months = ["0" + str(i) if i < 10 else str(i) for i in range(1, 13)]
    years =  ["2020"]
    for year in years:
        for monthIndex in range(len(monthNames)):
            for dayName in getDaysOfMonthAsList(int(months[monthIndex]), int("2020")):
                folderNew = folder + "/" + year + "/" + monthNames[monthIndex] + "/" + "Day " + dayName
                if os.path.isdir(folderNew):
                    print("Inserting Data  from Folder:", folderNew)
                    print("---------------------------------------")
                    insertEveryJsonDocumentOfAFolderInDatabase(connection, folderNew, tableName)
                    print("")
                    print("---------------------------------------")
                    print("")
                    
def createFullTextIndexForDateColumn(connection, tableName, indexName, indexColumn):
    query = "CREATE FULLTEXT INDEX IF NOT EXISTS " + indexName
    query += " ON " + tableName +  "(" + indexColumn +");"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
                    
# main function of program
if __name__ == "__main__":
    configData = json.load(open("config.json"))
    host = configData["host"]
    user = configData["user"]
    password = configData["password"]
    database = configData["database"]
   
    tableNames = [configData["sqlTable"]]
    templates = ["build/tableTemplateFromData.json"]
    
    rootDir = "twitterData"
    
    """
    main driver part for inserting all data 
    """
    connection = createConnectionToMySQLDatabase(host, user, password, database)
    connection.set_charset_collation('utf8mb4', "utf8mb4_unicode_ci")
    createTableTemplateFromData(rootDir)
    createTables(connection, tableNames, templates)   
    executeInsersionOfAllJsonInDatabase(connection, rootDir, tableNames[0])
    createFullTextIndexForDateColumn(connection, tableNames[0], "DateSearch", "created_at")
    closeConnectionToMySQLDatabase(connection)

