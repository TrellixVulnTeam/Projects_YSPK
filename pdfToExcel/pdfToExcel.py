#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from tabula import read_pdf
import os
from tabula import convert_into
from PyPDF2 import PdfFileReader

class PDFtoExelConverter:
    def __init__(self, inputFile):
        self.pdfTitle = self.getPDFTitle(inputFile)
        self.createDir("output")
        self.createDir("output/" + self.pdfTitle)
        self.convertTablesToExcel(inputFile, self.pdfTitle)
    
    def createDir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            
    def getPDFPageCount(self, file):
        pdf = PdfFileReader(open(file,'rb'))
        return pdf.getNumPages() + 1
    
    def getPDFTitle(self, file):
         return os.path.splitext(os.path.basename(file))[0]
    
    def convertTablesToExcel(self, inputFile, pdfTitle):
        pageCount = self.getPDFPageCount(inputFile)
        for pageNumber in range(1, pageCount):
            outputFile = "output/"+ pdfTitle + "/page-" + str(pageNumber) + ".csv"
            print("Converting Page", pageNumber, "to csv...")
            convert_into(inputFile, outputFile, pages = pageNumber)
