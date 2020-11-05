#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import json


class AdvancedTextFilterSystem:
    def __init__(self, filePath, savePath, query):
        self.fileLines = list(dict.fromkeys(open(filePath).readlines()))
        self.savePath = savePath
        self.query = query
        self.functions = list()
        self.filterData = json.load(filePath)

    def getFilter(self):
        return self.filterData[self.query.split(":")[0]]

    def filterFunctionsFromText(self):
        searchString = self.getFilter()
        for line in self.fileLines:
            if re.search(searchString, line):
                self.functions.append(line)

    def writeFunctionsAndExplanationToFile(self, file):
        for i in range(1, len(self.functions)-1):
            funcIndex = self.fileLines.index(self.functions[i])
            while True:
                if funcIndex == self.fileLines.index(self.functions[i+1]):
                    break
                file.write(self.fileLines[funcIndex])
                funcIndex += 1
            file.write("\n")

    def executeFitering(self):
        file = open(self.savePath, "w", encoding="utf8")
        self.filterFunctionsFromText()
        self.writeFunctionsAndExplanationToFile(file)
        file.close()
