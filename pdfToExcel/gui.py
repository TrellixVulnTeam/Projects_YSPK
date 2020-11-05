#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pdfToExcel
import tkinter
from tkinter import filedialog as fd 
from tkinter import messagebox


class GUI:
    def __init__(self, title):
        self.pdfFile = ""
        self.rootWindow = tkinter.Tk()
        self.rootWindow.wm_title(title)
        self.rootWindow.geometry("300x100")
        self.createGUIElements(self.rootWindow)
        tkinter.mainloop()
        
    def callBackOpen(self):
        self.pdfFile = fd.askopenfilename(filetypes = [("PDF Files", "*.pdf")])
    
    def callBackStartConverting(self):
        if self.pdfFile != "":
            converterObject = pdfToExcel.PDFtoExelConverter(self.pdfFile)
            messagebox.showinfo("INFO BOX", "Done Converting!")
        
        
    def textButtonCombinationField(self, window, labelText, buttonText, row, callback):
         tkinter.Label(window, text = labelText).grid(row = row)
         entryField = tkinter.Button(window, text = buttonText, command = callback )
         entryField.grid(row = row, column = 1)
         entryField.focus_set()
         return entryField
        
    def createGUIElements(self, window):
        openFileButton = self.textButtonCombinationField(window, "Open File:", 
                                                         "Choose File", 0, 
                                                         self.callBackOpen)
        startConvertingButton = tkinter.Button(window, text = "Start Converting", 
                       command = self.callBackStartConverting)
        startConvertingButton.grid(row = 1, column = 0)


