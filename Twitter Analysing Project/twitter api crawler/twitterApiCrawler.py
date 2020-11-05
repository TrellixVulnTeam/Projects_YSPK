#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMPORTANT NOTE: set innodb_lock_wait_timeout=100; 
must be exuted in the mySQL/MariaDB to chnage the timeout config
before starting the recrawler

general purpose: This is a Recrawler which recrawls specific data, found in 
the variableNames field in the main function, from the Twitter API and 
creates an SQL UPDATE statement and executes the statement for each Document
returned by the Twitter API

Known Issues: the Twitter API forbids the connection after 10K - 12K 
queries that was send, no reconnect possible for an undefined time

Possible Solutions for Known Issues: If the restriction is on IP Level
use a TOR-network like solution for cycling around 3 proxies and connect to 
new proxies after new authentication

If the restriction is on account level: pay for more queries or upgrade account 
"""

import json
import databaseConnector as dbc
from requests_oauthlib import OAuth1Session
import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

"""
this function automates the authentication by using a browser bot
who automatically inputs the twitter login data found in the twitterConfig.json 
and the authentication code resived after simulating a iser who pressed enter
if there are too many logins attempts the bot will be asked to to verify this login
with a second login because of the we use email instead of the useranme
so the bot can easil enter both logins if asked

IMPORTANT NOTE: this code must be updated if the website code or structure 
changes especially the line 69 with the code =
because it uses a css selector to get the code under this path 
'#oauth_pin > p > kbd > code
"""
def automateOauthForTwitterApiWithSelenium(username, password, oauthLink):
    tooManyLoginsSubstringURL = "https://twitter.com/login?username_disabled=true&redirect_after_login="
    firefoxOptions = Options()
    firefoxOptions.headless = True
    driver = webdriver.Firefox(options = firefoxOptions, 
                               executable_path=GeckoDriverManager().install())
    driver.get(oauthLink)
    username_field = driver.find_element_by_name("session[username_or_email]")
    password_field = driver.find_element_by_name("session[password]")
    username_field.send_keys(username)
    driver.implicitly_wait(1)
    password_field.send_keys(password, Keys.ENTER)
    driver.implicitly_wait(30)
    
    time.sleep(4)
    if tooManyLoginsSubstringURL in driver.current_url:
        username_fieldA = driver.find_element_by_name("session[username_or_email]")
        password_fieldA = driver.find_element_by_name("session[password]")
        username_fieldA.send_keys(username)
        driver.implicitly_wait(1)
        password_fieldA.send_keys(password, Keys.ENTER)
        driver.implicitly_wait(30)
        time.sleep(4)
        driver.find_element_by_tag_name('body').send_keys(Keys.ENTER)
        time.sleep(4)
    
    code = driver.find_element_by_css_selector('#oauth_pin > p > kbd > code').text
    return code

"""
this function gets the id_str (id as string) for all records in the mySQL/mariaDB 
database and returns the result

The Twitter API uses the id_str field to identify the record, the field id is not
by the Twitter API in queries
"""
def getAllTextsFromMySQLDatabase(connection, tableName):
    query = "SELECT id_str, " + tableName + "_ID"
    query += " FROM " + tableName + " WHERE id_str IS NOT NULL;"
    resultNotList = connection.executeQuery(query) 
    return resultNotList

"""
this function builds the SQL UPDATE Statement, the function also just 
updates available variables for that it checks if the current variable name is
in the recieved data, the targetVariableValuePair contais the key value pair
for identifiing the to be updated record
"""
def buildUpdateStatement(tableName, variableNames, variableValues, targetVariableValuePair):
    query = "UPDATE " + tableName + " SET "
    targetValue = (str(targetVariableValuePair[1]) if type(targetVariableValuePair[1]) != type(str()) 
                 else "'" +  targetVariableValuePair[1] + "'")
    for i in range(len(variableNames)):
        value = (str(variableValues[i]) if type(variableValues[i]) != type(str()) 
                 else "'" +  variableValues[i] + "'")
        query += variableNames[i]  + " = " + value
        if variableNames[i] != variableNames[-1]:
            query += ", "
    query += " WHERE " + targetVariableValuePair[0] + " = "
    query += targetValue + ";"
    return query

"""
this function sends the SQL UPDATE Statement to the mySQL/mariaDB Database
and executes it
"""
def updateSingleRecord(connection, updateQuery):
    cursor = connection.getDatabaseConnection().cursor()
    cursor.execute(updateQuery)
    connection.getDatabaseConnection().commit()
    cursor.close()
    
"""
this function is for connecting to the Twitter API and returns an request object
to send queries

IMPORTANT NOTE: If the request_token_url or base_authorization_url changes
the  code must be updated
"""    
def getAccesToTwitterAPI(consumer_key, consumer_secret, twitterLoginData):
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')
    print("Got OAuth token: %s" % resource_owner_key)

    # # Get authorization
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    authorization_url = oauth.authorization_url(base_authorization_url)
    print('Please go here and authorize: %s' % authorization_url)
    print("Bypassing manual Authorization...")
    verifier = automateOauthForTwitterApiWithSelenium(twitterLoginData[0], 
                                                      twitterLoginData[1], 
                                                      authorization_url)
    print("your code is:", verifier)
    #input('Paste the PIN here: ')
    
    

    # # Get the access token
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(consumer_key,
                          client_secret=consumer_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens['oauth_token']
    access_token_secret = oauth_tokens['oauth_token_secret']

    # Make the request
    oauth = OAuth1Session(consumer_key,
                          client_secret=consumer_secret,
                          resource_owner_key=access_token,
                          resource_owner_secret=access_token_secret)
    return oauth

"""
this function executes the complete update for all ids in idList, if the rate 
limit is reached zhe function automatically waits 16 minutes and reconnects to 
the Twitter API server

this function includes crawling the data from the Twitter API and updating
the mySQL/mariaDB database

IMPORTANT NOTE: if the Twitter API endpoints changed this code must be
updated
"""
def executeUpdate(apiConnection, databaseConnection, idList, variableNames, 
                  tableName, consumer_key, consumer_secret, twitterLoginData):
    for ID in idList:
        print("ID of Record to be updated:", ID[0])
        realVariableNames, realVariableValues = list(), list()
        targetVariableValuePair = [tableName + "_ID", ID[1]]
        params = {"id": ID[0].replace("\"","")}
        print("Parameter to be send:", params)
        response = apiConnection.get("https://api.twitter.com/1.1/statuses/show.json", 
                                     params = params)
        if int(response.status_code) == 429:
            print("Limit reached waiting 16 Minutes then sending again...")
            time.sleep(960)
            apiConnection = getAccesToTwitterAPI(consumer_key, consumer_secret, twitterLoginData)
            response = apiConnection.get("https://api.twitter.com/1.1/statuses/show.json", 
                                     params = params)
        print("Twitter API Response status: %s" % response.status_code)
        data = json.loads(response.text)
        for variable in variableNames:
            if variable in list(data.keys()):
                if data[variable] != 0:
                    realVariableNames.append(variable)
                    realVariableValues.append(data[variable])
        if realVariableNames:
            print("Variables to be updated:", realVariableNames)
            updateQuery = buildUpdateStatement(tableName, realVariableNames, 
                                           realVariableValues, 
                                           targetVariableValuePair)
            print(updateQuery)
            updateSingleRecord(databaseConnection, updateQuery)
        print("Record with", ID[0], "updated")
    print("execution of SQL Table Update finished")
        

#general main of the program
if __name__ == "__main__":
    #config files as Json Files
    databaseConfigData = json.load(open("databaseConfig.json"))
    twitterApiConfigData = json.load(open("twitterApiConfig.json"))
    
    #mySQL/mariaDB configuration  Data
    host = databaseConfigData["host"]
    user = databaseConfigData["user"]
    password = databaseConfigData["password"]
    database = databaseConfigData["database"]
    sqlTable = databaseConfigData["sqlTable"]
    
    #Twitter API configuration  Data
    twitterLoginData = [twitterApiConfigData["email"], 
                        twitterApiConfigData["password"]]
    consumer_key = twitterApiConfigData["consumer_key"]
    consumer_secret = twitterApiConfigData["consumer_secret"]
    
    #variables to be updated if existing in the crawled data
    variableNames = ["retweet_count", "favorite_count", 
                     "reply_count", "quote_count"]
    
    #Connect to mySQL/mariaDB Database
    print("Connecting to mySQL/MariaDB Database...")
    connection = dbc.DatabaseConnector(host, user, password, database)
    connection.connectToDatabase()
    
    #Connect to Twitter API endpoint
    print("Connecting tp Twitter API...")
    apiConnection = getAccesToTwitterAPI(consumer_key, consumer_secret, twitterLoginData)
    
    #get all the ids to be updated from mySQL/mariaDB database
    print("Getting all Twitter Tweet IDs that are to be updated...")
    idList = getAllTextsFromMySQLDatabase(connection, sqlTable)
    
    print("Number of IDs found:", len(idList))
    
    #Execute the complete Update of the recrawled Data
    print("Executing the Updates...")
    executeUpdate(apiConnection, connection, idList, variableNames, sqlTable,
                  consumer_key, consumer_secret, twitterLoginData)
    
    #Disconnect from mySQL/mariaDB Database
    connection.disconnectFomDatabase()
    
    