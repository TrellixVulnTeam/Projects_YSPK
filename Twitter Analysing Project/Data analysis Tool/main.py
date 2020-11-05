#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Purpose: it is the main program which will the user start
later on the gui will also be called here
"""
import databaseConnector as dbc
import plotter
import json

# main
if __name__ == "__main__":   
    # the main driver part of the program 
    configData = json.load(open("config.json"))
    host = configData["host"]
    user = configData["user"]
    password = configData["password"]
    database = configData["database"]
    sqlTable = configData["sqlTable"]
    connection = dbc.DatabaseConnector(host, user, password, database)
    connection.connectToDatabase()
    plotterObject = plotter.Plotter(connection, sqlTable)
    plotterObject.mainPlotAll("2020")