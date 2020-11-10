#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Purpose: a class for connecting to a mariaDB/mySQL database
and handling the execution of a SQL Query and getting it's result 
"""
import mysql.connector as mc

class DatabaseConnector:
    # init function
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.databaseConnection = None
    
    # funtion for connecting to the mariaDB/mySQL database
    def connectToDatabase(self):
        self.databaseConnection = mc.connect (host = self.host, user = self.user,
                       passwd = self.password, db = self.database)
        self.databaseConnection.set_charset_collation('utf8mb4', "utf8mb4_unicode_ci")
    
    # funtion for executing the SQL-Query and getting it's result        
    def executeQuery(self, query):
        cursor = self.databaseConnection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
     # funtion for executing a SQL Update query or a SQL INSERT INTO query
    def updateQuery(self, query):
        cursor = self.databaseConnection.cursor()
        cursor.execute(query)
        self.databaseConnection.commit()
    
    # funtion for disconnecting from the mariaDB/mySQL database
    def disconnectFomDatabase(self):
        self.databaseConnection.close()
        