#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import py_files.controller as con

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: argument missing")
    elif sys.argv[1] == "demoMode":
        testQueries = list()
        testQueries.append("python:math:how to get sine from x")
        testQueries.append("c++:algorithm swap:how to use swap()")
        testQueries.append("java:math:how to get pow from x")
        print("Bot.Docs B Demo")
        print("")
        for query in testQueries:
            c = con.ControlManager(query)
            c.initSession()
            c.crawlQuery()
            result = c.executeFiltering()
            c.closeSession()
            print("Your Query:", query)
            print("")
            print("Your Result:", result)
            print("")
    elif sys.argv[1] == "userMode":
        while True:
            print("Bot.Docs B Demo")
            print("")
            print("Your Query (Type exit to exit): ", end='')
            query = input()
            if query == "exit":
                break
            else:
                c = con.ControlManager(query)
                c.initSession()
                c.crawlQuery()
                result = c.executeFiltering()
                c.closeSession()
                print("Your Query:", query)
                print("")
                print("Your Result:", result)
                print("")
    else:
        print("ERROR: wrong argument. arguments are demoMode or userMode.")
