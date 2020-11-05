#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
import py_files.filesystemhandler as fsh
import py_files.controller as cont


class TestController(unittest.TestCase):
    def testInit(self):
        query = "python:math:how to use sine"
        con = cont.ControlManager(query)
        self.assertEqual(con.query, query)
        self.assertEqual(con.filterObject, None)
        self.assertEqual(con.crawlerObject, None)
        self.assertIs(type(con.fileHandler), fsh.FileSystemHandler)

    def testInitSession(self):
        query = "python:math:how to use sine"
        con = cont.ControlManager(query)
        con.initSession()
        self.assertTrue(os.path.isdir(con.fileHandler.getRootDirectory()))

    def testCrawlQuery(self):
        query = "python:math:how to use sine"
        con = cont.ControlManager(query)
        con.initSession()
        con.crawlQuery()
        filePath = con.fileHandler.getSearchFilePath("python", "math.txt")
        self.assertTrue(filePath)
        fileTest = open(filePath).read()
        self.assertTrue("<html>" not in fileTest)
        self.assertTrue("sin" in fileTest and "cos" in fileTest)

    def testExecuteFiltering(self):
        query = "python:math:how to use sine"
        con = cont.ControlManager(query)
        con.initSession()
        con.crawlQuery()
        result = con.executeFiltering()
        self.assertTrue("sin(x)" in result)

    def testCloseSession(self):
        query = "python:math:how to use sine"
        con = cont.ControlManager(query)
        con.initSession()
        con.crawlQuery()
        con.executeFiltering()
        con.closeSession()
        rootDir = con.fileHandler.getRootDirectory()
        self.assertTrue(os.path.exists(rootDir))
        self.assertTrue(os.path.isdir(rootDir) and not os.listdir(rootDir))


if __name__ == "__main__":
    unittest.main()
