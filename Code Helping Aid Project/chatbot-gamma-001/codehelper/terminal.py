#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import py_files.controller as con

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: argument missing")
    else:
        c = con.ControlManager(sys.argv[1])
        c.initSession()
        c.crawlQuery()
        result = c.executeFiltering()
        #c.closeSession()
        print(result)
