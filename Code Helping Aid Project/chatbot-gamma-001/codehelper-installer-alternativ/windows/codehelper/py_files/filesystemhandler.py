#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class FileSystemHandler:
    def __init__(self):
        self.createRootDirectory()

    def createRootDirectory(self):
        if not os.path.isdir(self.getRootDirectory()):
            os.mkdir(self.getRootDirectory())

    def getRootDirectory(self):
        rootDir = os.getcwd() + self.getSlashForOsVersion() + "data"
        return rootDir

    def getSlashForOsVersion(self):
        if os.name == "posix":
            return "/"
        return "\\"

    def checkDirElseMkDir(self, folder):
        if not os.path.isdir(folder):
            os.mkdir(folder)

    def getSearchFilePath(self, subdir, filename):
        searchFilePath = self.getRootDirectory() + self.getSlashForOsVersion()
        searchFilePath += subdir + self.getSlashForOsVersion() + filename
        return searchFilePath

    def deleteSessionTempFiles(self, folder):
        for filename in os.listdir(folder):
            path = folder + self.getSlashForOsVersion() + filename
            if os.path.isdir(path):
                self.deleteSessionTempFiles(path)
                os.rmdir(path)
            else:
                os.remove(path)
