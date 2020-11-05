#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
import py_files.filesystemhandler as fsh


class TestClient(unittest.TestCase):
    def testInit(self):
        f = fsh.FileSystemHandler()
        self.assertTrue(os.path.isdir(f.getRootDirectory()))

    def testGetRootDirectory(self):
        rootDir = "/home/philipp/Dokumente/5. Semester/"
        rootDir += "Softwarepraktikum_Chatbot/chatbot-alpha/"
        rootDir += "chatbot-alpha-001/tests/data"
        f = fsh.FileSystemHandler()
        self.assertEqual(f.getRootDirectory(), rootDir)

    def testGetSlashForOsVersion(self):
        f = fsh.FileSystemHandler()
        self.assertEqual(f.getSlashForOsVersion(), "/")

    def testCheckDirElseMkDir(self):
        f = fsh.FileSystemHandler()
        testFolder = f.getRootDirectory()
        testFolder += f.getSlashForOsVersion() + "testIfMkDir"
        f.checkDirElseMkDir(testFolder)
        self.assertTrue(os.path.isdir(testFolder))

    def testGetSearchFilePath(self):
        f = fsh.FileSystemHandler()
        subdir = "c++"
        filename = "vector.txt"
        filePath = f.getRootDirectory()
        filePath += f.getSlashForOsVersion()
        filePath += subdir + f.getSlashForOsVersion() + filename
        self.assertEqual(f.getSearchFilePath(subdir, filename), filePath)

    def testDeleteSessionTempFiles(self):
        f = fsh.FileSystemHandler()
        dataDir = f.getRootDirectory()
        f.deleteSessionTempFiles(dataDir)
        testDir = dataDir + f.getSlashForOsVersion() + "testIfMkDir"
        self.assertFalse(os.path.isdir(testDir))


if __name__ == "__main__":
    unittest.main()
