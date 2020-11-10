#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Purpose: craete an API which manges the article Table
"""
import flask
import json
from flask import request, jsonify
import datetime
import databaseConnector as dbc

#define the global flask enviroment
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#get teh database connection config from config.json
def getDataBaseConnection():
    configData = json.load(open("config.json"))
    host = configData["host"]
    user = configData["user"]
    password = configData["password"]
    database = configData["database"]
    sqlTable = configData["sqlTable"]
    connection = dbc.DatabaseConnector(host, user, password, database)
    return connection, sqlTable

#this function builds a SQL Select Query from a Python dictionary
def buildSQLSelectQueryFromDict(dictionary, sqlTable):
    query = ("SELECT User.forname, User.surname, Article.name, " + 
                 "Article.creationdate, Article.publicationdate FROM User, " + 
                 "Article, ArticleUser WHERE ArticleUser.userid = User.id " +
                 "AND ArticleUser.articleid = Article.id AND Article.isdelete = 0 AND ")
    for key in dictionary.keys():
        query += key + " = " + dictionary[key]
        if list(dictionary.keys())[-1] != key: query += " AND "
    query += ";"
    return query

#this function builds a SQL Delete Query from a Python dictionary (Soft delete)
def buildSQLDeleteQueryFromDict(dictionary):
    query = "UPDATE User, ArticleUser, Article SET isdelete = 1"
    query += (" WHERE ArticleUser.userid = User.id " +
                 "AND ArticleUser.articleid = Article.id AND Article.isdelete = 0")
    query += " AND Article.name = " + str(dictionary["name"]) + ";"
    return query

#this function builds a SQL INSERT INTO Query from a Python dictionary
def buildSQLInsertIntoQueryFromDict(dictionary, sqlTable):
    query = "INSERT INTO " + sqlTable + " ("
    for key in dictionary.keys():
        query += str(key)
        if list(dictionary.keys())[-1] != key: query += ","
    query += ") VALUES ("
    for key in dictionary.keys():
        query += str(dictionary[key])
        if list(dictionary.keys())[-1] != key: query += ","
    query += ");"
    return query

#this function builds a SQL Update Query from a Python dictionary
def buildSQLUpdateQueryFromDict(dictionary, newPossibleArticleName):
    query = "UPDATE User, ArticleUser, Article SET "
    for key in dictionary.keys():
        if key == "name" and newPossibleArticleName is not None:
            query += str(key) + " = " + str(newPossibleArticleName)
        else:
            query += str(key) + " = " + str(dictionary[key]) 
        if list(dictionary.keys())[-1] != key: query += ","
    query += (" WHERE ArticleUser.userid = User.id " +
                 "AND ArticleUser.articleid = Article.id AND Article.isdelete = 0"
                 + " AND Article.name = ")
    query += str(dictionary["name"]) + ";"
    return query

#this function gets the columnnames which are aloowed to be displayed
def getColumnNames():
    columnNames = ["forname", "surname", "name", "creationdate", "publicationdate"]
    return columnNames

#this function builds a dictionary of key value pairs
def buildResultDictionaryFromLists(keys, values):
    resultDict = dict()
    for i in range(len(keys)):
        resultDict[keys[i]] = values[i]
    return resultDict

#this function converts a list of lists to a list of dicts
def rebuildResultsFromListsOfListsToListsOfDicts(columnNames, result):
    resultListOfDicts = list()
    for i in range(len(result)):  
        tempDict = buildResultDictionaryFromLists(columnNames, result[i])
        resultListOfDicts.append(tempDict)
    return resultListOfDicts

def getUserIDAndIsAuthor(queryParameters, connection):
    userQuery = ("SELECT id, isauthor FROM User WHERE forname = " + 
                 queryParameters["forname"] + " AND surname = " + 
                 queryParameters["surname"])
    result = connection.executeQuery(userQuery)
    return result[0][0], result[0][1]

def createNewArticleUserEntry(userId, articleId, connection):
    query = ("INSERT INTO ArticleUser (userid, articleid) Values (" + 
             str(userId) + ", "  + str(articleId) + ");")
    connection.updateQuery(query)
    
def getArticleIdByName(connection, name):
    query = ("SELECT Article.id FROM Article WHERE "
            "Article.isdelete = 0 AND "
            + "Article.name = " + name + ";")
    return connection.executeQuery(query)[0][0]

def saveNewArticleNameIfPresent(dictionary):
    if "name" in list(dictionary.keys()):
        return dictionary["name"]
    else:
        return None
    
def dateChecker(dateString):
    dateString = dateString.replace('"', "")
    dateSplit = dateString.split("-")
    if len(dateSplit) != 3:
        return False
    try:
        datetime.datetime(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]))
    except ValueError:
        return False
    return True

def stringChecker(string):
    try:
        str(string)
    except ValueError:
        return False
    return True
    
def getColumnPythonTypeMapper():
    return {"name" : stringChecker, "text" : stringChecker, "creationdate" : dateChecker,
            "publicationdate" : dateChecker, "forname" : stringChecker, 
            "surname" : stringChecker}
    
def validateRightTypeOfUserInputReturnTrueIfNoProblems(dictionary):
    mapper = getColumnPythonTypeMapper()
    for key in dictionary.keys():
        if not mapper[key](dictionary[key]):
            return False
    return True

def getSetOfValidURLNames():
    return {"forname", "surname", "name", "creationdate", "publicationdate", "text"}

def validatePermittedVariableNamesInURL(dictionary):
    dictKeysSet = set(list(dictionary.keys()))
    resultSet = dictKeysSet - getSetOfValidURLNames()
    if resultSet:
        return False
    return True

def validateMustHaveVariablesInURL(dictionary, mustHaveVariableList):
    for key in mustHaveVariableList:
        if not key in list(dictionary.keys()):
            return False
    return True

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

def userNotPermittedToCreateArticle(e):
    return "<h1>Errror</h1><p>User is not permitted to create Articles</p>"

def userNotPermittedToDeleteOrUpdateArticle(e):
    return "<h1>Errror</h1><p>User is not permitted to delete or update this article</p>"

def userInputValuesOfFalseType(e):
    return "<h1>Errror</h1><p>UserInput has wrong Types</p>"

def userInputHasWrongvariableNameInURL(e):
    return "<h1>Errror</h1><p>UserInput has wrong Variable Names</p>"

def userInputHasMissingMustHaveVariableNameInURL(e, variableList):
    return ("<h1>Errror</h1><p>UserInput has missing must have Variable Names: " +
            ", ".join(variableList) + "</p>")

def checkIfAuthorIsCreatorOfSpecificArticle(userId, articleId, connection):
    query = ("SELECT userid FROM ArticleUser WHERE userid = " + str(userId) +
             " AND articleid = " + str(articleId)  + ";")
    result = connection.executeQuery(query)
    if not result:
        return False
    return True
    

@app.route('/', methods=['GET'])
def home():
    return "<h1>Test API</h1><p>This site is a prototype API</p>"

"""
Usage: type host:port/api/v1/resources/article/all into the browser to recieve all 
articles in the database that are not soft deleted
"""
@app.route('/api/v1/resources/article/all', methods=['GET'])
def apiAll():
    columnNames = getColumnNames()
    connection, sqlTable = getDataBaseConnection()
    connection.connectToDatabase()
    query = ("SELECT User.forname, User.surname, Article.name, " + 
                 "Article.creationdate, Article.publicationdate FROM User, " + 
                 "Article, ArticleUser WHERE ArticleUser.userid = User.id " +
                 "AND ArticleUser.articleid = Article.id AND Article.isdelete = 0;")
    result = connection.executeQuery(query)
    connection.disconnectFomDatabase()
    result = rebuildResultsFromListsOfListsToListsOfDicts(columnNames, result)
    return jsonify(result)

"""
Usage: type host:port/api/v1/resources/article?yourvariable=yourvalue
into the browser to recieve articles in the database with the specifications
you entered and which are not soft deleted
"""
@app.route('/api/v1/resources/article', methods=['GET'])
def apiSelectFilter():
    columnNames = getColumnNames()
    queryParameters = request.args.to_dict()
    if not queryParameters:
        return page_not_found(404)
    if not validatePermittedVariableNamesInURL(queryParameters):
        return userInputHasWrongvariableNameInURL(200)
    if not validateRightTypeOfUserInputReturnTrueIfNoProblems(queryParameters):
        return userInputValuesOfFalseType(300)
    connection, sqlTable = getDataBaseConnection()
    connection.connectToDatabase()
    query = buildSQLSelectQueryFromDict(queryParameters, sqlTable)
    result = connection.executeQuery(query)
    connection.disconnectFomDatabase()
    result = rebuildResultsFromListsOfListsToListsOfDicts(columnNames, result)
    return jsonify(result)

"""
Usage: type host:port/api/v1/resources/test/delete?forname=yourvalue&
surname=yourvalue&name=yourarticlename
into the browser to recieve articles in the database with the specifications
you entered and which are not soft deleted
"""
@app.route('/api/v1/resources/test/delete', methods=['GET'])
def deleteSpecificEntries():
    mustHaveVariables = ["forname", "surname", "name"]
    queryParameters = request.args.to_dict()
    if not queryParameters:
        return page_not_found(404)
    if not validateMustHaveVariablesInURL(queryParameters, mustHaveVariables) :
        return userInputHasMissingMustHaveVariableNameInURL(100, mustHaveVariables)
    if not validatePermittedVariableNamesInURL(queryParameters):
        return userInputHasWrongvariableNameInURL(200)
    if not validateRightTypeOfUserInputReturnTrueIfNoProblems(queryParameters):
        return userInputValuesOfFalseType(300)
    connection, sqlTable = getDataBaseConnection()
    connection.connectToDatabase()
    userId, isAuthor = getUserIDAndIsAuthor(queryParameters, connection)
    articleId = getArticleIdByName(connection, queryParameters["name"])
    if not checkIfAuthorIsCreatorOfSpecificArticle(userId, articleId, connection):
        return userNotPermittedToDeleteOrUpdateArticle(420)
    query = buildSQLDeleteQueryFromDict(queryParameters)
    connection.updateQuery(query)
    connection.disconnectFomDatabase()
    return "<h1>Delete Request</h1><p>" + query + "</p>"

"""
Usage: type host:port/api/v1/resources/article/create?forname=yourvalue&
surname=yourvalue&name=yourarticlename&creationdate=yourdate
into the browser to recieve articles in the database with the specifications
you entered and which are not soft deleted
"""
@app.route('/api/v1/resources/article/create', methods=['GET'])
def createSpecificEntries():
    userKeys = ["forname", "surname"]
    mustHaveVariables = ["forname", "surname", "name", "creationdate"]
    queryParameters = request.args.to_dict()
    if not queryParameters:
        return page_not_found(404)
    if not validateMustHaveVariablesInURL(queryParameters, mustHaveVariables) :
        return userInputHasMissingMustHaveVariableNameInURL(100, mustHaveVariables)
    if not validatePermittedVariableNamesInURL(queryParameters):
        return userInputHasWrongvariableNameInURL(200)
    if not validateRightTypeOfUserInputReturnTrueIfNoProblems(queryParameters):
        return userInputValuesOfFalseType(300)
    connection, sqlTable = getDataBaseConnection()
    connection.connectToDatabase()
    userId, isAuthor = getUserIDAndIsAuthor(queryParameters, connection)
    if isAuthor == 0:
        return userNotPermittedToCreateArticle(444)
    for key in userKeys:
        queryParameters.pop(key, None)
    query = buildSQLInsertIntoQueryFromDict(queryParameters, sqlTable)
    connection.updateQuery(query)
    articleId = connection.executeQuery("SELECT LAST_INSERT_ID();")[0][0]
    createNewArticleUserEntry(userId, articleId, connection)
    connection.disconnectFomDatabase()
    return "<h1>Create Request</h1><p>" + query + "</p>"

"""
Usage: type host:port//api/v1/resources/article/edit/youarticlename?
forname=yourvalue&surname=yourvalue&otheroptionalvalues
into the browser to recieve articles in the database with the specifications
you entered and which are not soft deleted
"""
@app.route('/api/v1/resources/article/edit/<article>', methods=['GET'])
def updateSpecificEntries(article):
    userKeys = ["forname", "surname"]
    mustHaveVariables = ["forname", "surname"]
    queryParameters = request.args.to_dict()
    if not queryParameters:
        return page_not_found(404)
    if not validateMustHaveVariablesInURL(queryParameters, mustHaveVariables) :
        return userInputHasMissingMustHaveVariableNameInURL(100, mustHaveVariables)
    if not validatePermittedVariableNamesInURL(queryParameters):
        return userInputHasWrongvariableNameInURL(200)
    if not validateRightTypeOfUserInputReturnTrueIfNoProblems(queryParameters):
        return userInputValuesOfFalseType(300)
    newPossibleArticleName = saveNewArticleNameIfPresent(queryParameters)
    queryParameters["name"] ="\"" + article + "\""
    connection, sqlTable = getDataBaseConnection()
    connection.connectToDatabase()
    userId, isAuthor = getUserIDAndIsAuthor(queryParameters, connection)
    articleId = getArticleIdByName(connection, queryParameters["name"])
    if not checkIfAuthorIsCreatorOfSpecificArticle(userId, articleId, connection):
        return userNotPermittedToDeleteOrUpdateArticle(420)
    for key in userKeys:
        queryParameters.pop(key, None)
    query =  buildSQLUpdateQueryFromDict(queryParameters, newPossibleArticleName)
    connection.updateQuery(query)
    connection.disconnectFomDatabase()
    return "<h1>Update Request</h1><p>" + query + "</p>"

   
if __name__ == "__main__":
    app.run()