#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General Purpose: a class creating the gui and managing the user input
general gui main
"""
import tkinter
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import weighingSchemes as ws
import filter as fs
import csv

class GUI:
    # init function for setting globals
    def __init__(self, title, dataBaseConnection, sqlTable):
        self.scheme = ws.WeighingSchemes(dataBaseConnection, sqlTable)
        self.filterObject = fs.Filter()
        self.rootWindow = tkinter.Tk()
        self.rootWindow.wm_title(title)
        self.rootWindow.geometry("800x200")
        self.rootWindowMenu = tkinter.Menu(self.rootWindow)
        self.rootWindow.config(menu = self.rootWindowMenu)
        self.createMenuFields(self.rootWindowMenu)
        self.createCreateComboBox()
        self.slideShowCounter = 0
        tkinter.mainloop()
        
    """
    a function for getting the headlines for the combobox
    """
    def getListOfHeadlinesOFallAnalyze(self):
        labels = ["Please choose an analysis Type:", 
                          "Frequency Analysis (Specific Date)", 
                          "Frequency Analysis (Week)",
                          "Frequency Analysis (Month)",
                          "Analysis of Workdays (Specific Date)",
                          "Analysis of Weekend (Specific Date)",
                          ("Analysis of the Difference between workdays and"
                           " weekends (Specific Date)"),
                          "Frequency Analysis sorted by Country (Specific Date)",
                          "Analysis Of Hashtags witheld by Country (Specific Date)",
                          "Analysis of Day/Night Cycle (Specific Date)",
                          "Analysis of most retweeted (Specific Date)",
                           "Analysis of most favorited (Specific Date)",
                            "Analysis of most replyed (Specific Date)",
                             "Analysis of most quoted (Specific Date)",
                             "Analysis of the difference in two dates"]
        return labels
    
    """
    this function mapps the headlines with an explaination for the user
    how to use the a specific analysis
    """
    def getHeadLinesToExplainationMapper(self):
        mapper = { "Please choose an analysis Type:" : "", 
                   "Frequency Analysis (Specific Date)" : 
                   "Date: Day/Month/Year, Display Limit: Integer",  
                   "Frequency Analysis (Week)" : 
                   "Date: Day/Month/Year, Display Limit: Integer",
                   "Frequency Analysis (Month)" : 
                   "Date: Month/Year, Display Limit: Integer",
                   "Analysis of Workdays (Specific Date)" :
                   "Date: Month/Year, Display Limit: Integer",
                   "Analysis of Weekend (Specific Date)" :
                   "Date: Day/Month/Year, Display Limit: Integer",
                   ("Analysis of the Difference between workdays and"
                   " weekends (Specific Date)") :
                   "Date: Month/Year, Display Limit: Integer",
                   "Frequency Analysis sorted by Country (Specific Date)" :
                   "Date: Day/Month/Year, Display Limit: Integer",
                   "Analysis Of Hashtags witheld by Country (Specific Date)" :
                   "Date: Month/Year, Display Limit: Integer",
                   "Analysis of Day/Night Cycle (Specific Date)" :
                   "Date: Day/Month/Year, Display Limit: Integer",
                   "Analysis of most retweeted (Specific Date)" :
                   "Date: Day/Month/Year, Display Limit: Integer",
                   "Analysis of most favorited (Specific Date)" :
                   "Date: Day/Month/Year, Display Limit: Integer",
                   "Analysis of most replyed (Specific Date)" :
                   "Date: Day/Month/Year, Display Limit: Integer",
                   "Analysis of most quoted (Specific Date)" : 
                   "Date: Day/Month/Year, Display Limit: Integer",
                   "Analysis of the difference in two dates" :
                   ("First Date: Day/Month/Year, Second Date: Day/Month/Year, "
                   "Display Limit: Integer")
                 }
        return mapper
    
    """
    this function mapps all one paramter function to the headlines
    """
    def getOnehistogramFunctioAndOneParameternMapper(self):
        mapper = {"Frequency Analysis (Specific Date)" : 
                  self.scheme.frequencyAnalysisWithParticularizedDate, 
                  "Frequency Analysis (Week)" :
                  self.scheme.frequencyAnalysisWithParticularizedDateSummedUpToWeek,
                  "Frequency Analysis (Month)" :
                  self.scheme.frequencyAnalysisWithParticularizedDateSummedUpToMonth,
                  "Analysis of Workdays (Specific Date)" : 
                  self.scheme.analysisOfWorkdaysForASpecificDate,
                  "Analysis of Weekend (Specific Date)" :
                  self.scheme.analysisOfWeekendaysForASpecificDate,
                  "Frequency Analysis sorted by Country (Specific Date)" :
                  self.scheme.analysisOfHashtagsForEachCountryOnaSpecificDateWithFrequency
                 }
        return mapper
    
    """
    this function mapps all two paramter function to the headlines
    """
    def getOnehistogramFunctioAndTwoParameternMapper(self):
        mapper = {"Analysis of most retweeted (Specific Date)" : 
                  self.scheme.analysisOfDataFRomASpecificDateWithTwitterCounter,
                  "Analysis of most favorited (Specific Date)" : 
                  self.scheme.analysisOfDataFRomASpecificDateWithTwitterCounter,
                  "Analysis of most replyed (Specific Date)" :  
                  self.scheme.analysisOfDataFRomASpecificDateWithTwitterCounter,    
                  "Analysis of most quoted (Specific Date)" : 
                  self.scheme.analysisOfDataFRomASpecificDateWithTwitterCounter
                 }
        return mapper
    
    """
    this function mis mapping the headline with the twitter counters in the sql
    database
    """
    def getOnehistogramFunctioAndTwoParameternCounterMapper(self):
        mapper = {"Analysis of most retweeted (Specific Date)" : "retweet_count",
                  "Analysis of most favorited (Specific Date)" : "favorite_count",
                  "Analysis of most replyed (Specific Date)" : "reply_count",   
                  "Analysis of most quoted (Specific Date)" : "quote_count"
                 }
        return mapper
    
    """
    this function is mapping the headlines with the functions that will be shown
    as a table with compares of content as content
    """
    def getFunctionsThatWillBeShownASCompareTable(self):
        mapper = {"Analysis of Day/Night Cycle (Specific Date)" :
                  self.scheme.analysisOfHashtagsDayNightCycleWithSpecificDate,
                  ("Analysis of the Difference between workdays and"
                   " weekends (Specific Date)") :
                      self.scheme.analysisOfDifferenceInHashtagsWorkdayAndWeekends,
                  "Analysis of the difference in two dates" : 
                  self.scheme.findNewHashtagsFomTwoDates,
                  "Analysis Of Hashtags witheld by Country (Specific Date)" :
                  self.scheme.analysisOfPostsWithHashtagsWithheldInCountriesOnASpecificDate
                  }
        return mapper
    
    """
    this function gets the table column names for a specific headline
    """
    def getLabelsForCompareTable(self):
        mapper = {"Analysis of Day/Night Cycle (Specific Date)" :
                  ["Hashtag", "Day", "Night"],
                  ("Analysis of the Difference between workdays and"
                   " weekends (Specific Date)") : ["Hashtag", "Workday", "Weekend"],
                  "Analysis of the difference in two dates" : 
                  ["Hashtag", "Old", "New"],
                  "Analysis Of Hashtags witheld by Country (Specific Date)" :
                  ["Country", "Witheld Hashtags"]
                  }
        return mapper
    
    """
    this function gets the axis names of the histogram for a specific headline
    """
    def getLabelForHistograms(self, date):
        mapper = {"Frequency Analysis (Specific Date)" : 
                  ["Frequency Analysis " + date, "Hashtags", "Amount"], 
                  "Frequency Analysis (Week)" :
                  ["Frequency Analysis (Week)" + date, "Hashtags", "Amount"],
                  "Frequency Analysis (Month)" :
                  ["Frequency Analysis " + date, "Hashtags", "Amount"],
                  "Analysis of Workdays (Specific Date)" : 
                  ["Frequency Analysis Workdays " + date, "Hashtags", "Amount"],
                  "Analysis of Weekend (Specific Date)" :
                  ["Frequency Analysis Weekend " + date, "Hashtags", "Amount"],
                  "Analysis of most retweeted (Specific Date)" :  
                  ["Analysis of Retweets" + date, "Hashtags", "Retweets"],
                  "Analysis of most favorited (Specific Date)" : 
                  ["Analysis of Favorits" + date, "Hashtags", "Favorited"],
                  "Analysis of most replyed (Specific Date)" : 
                  ["Analysis of Replys" + date, "Hashtags", "Replys"],
                  "Analysis of most quoted (Specific Date)" : 
                  ["Analysis of Quotes" + date, "Hashtags", "Quotes"]
                }
        return mapper
    
    """
    this function gets the date input and output formats for as specific
    headline
    """
    def getDateFormats(self):
        mapper = {"Analysis of Day/Night Cycle (Specific Date)" : 
                  ['%d/%m/%Y', '%b %d'],
                  ("Analysis of the Difference between workdays and"
                   " weekends (Specific Date)") : ['%m/%Y', '%b'],
                  "Frequency Analysis (Specific Date)" : ['%d/%m/%Y', '%b %d'], 
                  "Frequency Analysis (Week)" : ['%d/%m/%Y', '%b %d'],
                  "Frequency Analysis (Month)" : ['%m/%Y', '%b'],
                  "Analysis of Workdays (Specific Date)" : ['%m/%Y', '%b'],
                  "Analysis of Weekend (Specific Date)" : ['%m/%Y', '%b'],
                  "Analysis of most retweeted (Specific Date)" : 
                  ['%d/%m/%Y', '%b %d'],
                  "Analysis of most favorited (Specific Date)" : 
                  ['%d/%m/%Y', '%b %d'],
                  "Analysis of most replyed (Specific Date)" :
                  ['%d/%m/%Y', '%b %d'],   
                  "Analysis of most quoted (Specific Date)" : ['%d/%m/%Y', '%b %d'],
                  "Analysis of the difference in two dates" : ['%d/%m/%Y', '%b %d'],
                  "Analysis Of Hashtags witheld by Country (Specific Date)" :
                   ['%m/%Y', '%b'],
                   "Frequency Analysis sorted by Country (Specific Date)" : 
                   ['%d/%m/%Y', '%b %d']
                  }
        return mapper
    
    """
    this function is mapping the error codes with the error messages for the user
    inout fields
    """
    def userInputfFieldsErrorCodeErrorMessageMapper(self):
        mapper = {"limit not int" : 
                  ("The Entry for the  Display Limit is not an Integer. "
                   "Example 10"),
                  "limit <= 0" : 
                  ("The Entry for the  Display Limit must be greater than zero. "
                   "Example 10"),
                  "Date format" : 
                  ("Date must be like Day/Month/Year or Month/Year. "
                   "Example 01/01/2020")
                 }
        return mapper
    
    """
    this function is mapping the axis labels for a slidehow of histograms
    for a specific headline
    """
    def getAxisLabelsForSlidesShow(self, date):
        mapper = {"Frequency Analysis sorted by Country (Specific Date)" : 
                  [" " + date, "Hashtag", "Amount"]
                 }
        return mapper
    
    # a function for hetting the clicked item for the matplotlib toolbar
    def on_key_press(self, event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, canvas, toolbar)
        
    """
    this function checks if the string which the user entered is a valid
    date
    """    
    def checkDateFormating(self, date, dateFormat):
        try:
            self.filterObject.convertInputDateToUsableDate(date, 
                                                                  dateFormat[0],
                                                                  dateFormat[1])
        except ValueError:
            return True
        return False
    
    """
    this function checks if errors occured in the user input fields
    """    
    def ckeckUserInputFielsForErrors(self, args):
        errorList = list()
        dateFormat = self.getDateFormats()[args[1]]
        try:
             limit = (int(args[3].get()) if args[1] != 
             "Analysis of the difference in two dates" 
              else int(args[4].get()))
        except ValueError:
            errorList.append("limit not int")
        if not errorList:
            if limit <= 0:
                errorList.append("limit <= 0")
        if self.checkDateFormating(args[2].get(), dateFormat):
             errorList.append("Date format")
        if args[1] == "Analysis of the difference in two dates":
            if self.checkDateFormating(args[3].get(), dateFormat):
                errorList.append("Date format")
        return errorList
            
    
    # a function for getting all widgets on tkinter gui window    
    def getWidgetsOfWindow(self, window):
        templist = window.winfo_children()
        for item in templist:
            if item.winfo_children() :
                templist.extend(item.winfo_children())
        return templist
    
    # a function for setting the root window to its inital state
    def setRootWindowToInitalState(self, window):
        for item in self.getWidgetsOfWindow(window)[2:]:
            item.destroy()
    
    """
    this function deletes all child widhets of a tkinter window
    """        
    def deleteAllWidgetsOfAWindow(self, window):
        for item in self.getWidgetsOfWindow(window):
            item.destroy()
    
    """
    this function creates a list of matplotlib figures that will be later 
    on used to draw the plots in an tkinter gui
    """        
    def getFiguresForSlideShowFromDictAsList(self, dictionary, limit, reversing, axisLabels):
        figures = list()
        for key in dictionary:
            sortedDict = self.filterObject.sortDictionary(dictionary[key], reversing)
            keys = list(sortedDict.keys())[:limit]
            values = list(sortedDict.values())[:limit]
            labels = [key + axisLabels[0]] + axisLabels[1:]
            figures.append(self.getHistogramFigureSubPlot(keys, values, labels, colors = None))
        return figures
    
    """
    function for a creating a textinput field with a label with tkinter
    grid layout
    """
    def textInputCombinationField(self, window, labelText, row):
         tkinter.Label(window, text = labelText).grid(row = row)
         entryField = tkinter.Entry(window)
         entryField .grid(row = row, column = 1)
         entryField.focus_set()
         return entryField
     
    """
    a function for deleting all child widgets of a tkinter window
    starting from the second one 
    """ 
    def deleteAllWifgtesComingAfterTheFirst(self, window):
        widgets = self.getWidgetsOfWindow(window)[1:]
        for widget in widgets:
            widget.destroy()
            
    """
    this function creates the help menu shown in the gui
    """    
    def createMenuFields(self, menu):
        helpmenu = tkinter.Menu(menu)
        menu.add_cascade(label="Help", menu = helpmenu)
        helpmenu.add_command(label="Usage", command = self.createUsageHelpWindow)
        helpmenu.add_command(label="About", command = self.createAboutWindow)
            
    """
    this function creates an about window
    """    
    def createAboutWindow(self):
        aboutWindow = tkinter.Toplevel(self.rootWindow)
        aboutWindow.wm_title("About this Program")
        aboutWindow.geometry("300x100")
        textBox= tkinter.Text(aboutWindow)
        textBox.pack()
        textBox.configure(state='normal')
        textBox.insert(tkinter.END, "A Twitter Parser\nBy Wiedemann\n")
        textBox.configure(state='disabled')
        
    """
    this function is used when the user clicked in the comboBox in the 
    usage help window, it will show a usage help for a specific function
    """
    def callBackComboBoxUsage(self, event, window, comBox):
        self.deleteAllWifgtesComingAfterTheFirst(window)
        labelText =  self.getHeadLinesToExplainationMapper()[comBox.get()]
        label = tkinter.Label(master = window, text = labelText)
        label.grid(column=0, row=1)
        
    """
    this function creates the usage help window 
    """    
    def createUsageHelpWindow(self):
        usageWindow = tkinter.Toplevel(self.rootWindow)
        usageWindow.wm_title("Usage Help")
        usageWindow.geometry("600x100")
        labelsToChoose = self.getListOfHeadlinesOFallAnalyze()
        comboBox = ttk.Combobox(usageWindow, state = "readonly", 
                                values = labelsToChoose, width = 75)
        comboBox.grid(column=0, row=0)
        comboBox.current(0)
        comboBox.bind("<<ComboboxSelected>>", lambda event, window = usageWindow: 
                      self.callBackComboBoxUsage(event, window, comboBox))
            
    """
    this function creates a radio buttons with a specific label, used definig the 
    sorting order later on
    """ 
    def createRadioButtonWithLabel(self, window, buttonContend, labelText, row):
        v = tkinter.IntVar()
        v.set(1)
        tkinter.Label(window, text = labelText, justify = tkinter.LEFT, 
                      padx = 20).grid(row = row)
        for txt, val in buttonContend:
            tkinter.Radiobutton(window, text = txt, padx = 20, variable = v, 
                                value=val).grid(column = val, row = row)
        return v
    
    """
    this function gets the data from a tkinter treeview and puts each row
    in a list and stores each list an the same end list which will be 
    returned
    """
    def getDataForWritingItToCsvFile(self, table, headings):
        toWrite = list()
        toWrite.append(headings)
        for child in table.get_children():
            childContents = table.item(child)
            tempList = [childContents["text"]]
            for value in childContents["values"]:
                tempList.append(value)
            toWrite.append(tempList)
        return toWrite
    
    """
    this functin wriites a list of lists to csv file
    """
    def writeDataToCsvFile(self, fileName, toWrite):
        file = open(fileName, 'w')
        with file:
            writer = csv.writer(file)
            for row in toWrite:
                writer.writerow(row)
                
    """
    this function is used when the user clicked on the button to save 
    a tkinter treeview as a csv file, this function also calls
    a tkinter file dialog to get teh name and path of the file
    """
    def callBackSaveAsCsvFileForTables(self, table, headings):
        fileName = tkinter.filedialog.asksaveasfilename(filetypes = [('CSV File', '*.csv')])
        toWrite = self.getDataForWritingItToCsvFile(table, headings)
        if type(fileName) == type(str()) and fileName != '': 
            self.writeDataToCsvFile(fileName, toWrite)
        
    """
    this function shows the button for saving a tkinter treeview as a 
    csv file
    """    
    def showSaveAsCsvFileButtonForTables(self, window, table, labels):
        saveButton = tkinter.Button(window, text="Save as CSV File", command =
                                    lambda table = table, headings = labels: 
                                    self.callBackSaveAsCsvFileForTables(table, headings))
        saveButton.pack()
        
    """
    this function creates a tkinter treeview with a table like look and
    compares two avlues with each other
    """        
    def createCompareTable(self, window, labels,  listA, listB):
        table = ttk.Treeview(window)
        table["columns"] = tuple("#" + str(i) for i in range(1, len(labels)))
        allItems = list(set(listA + listB))
        for i in range(len(labels)):
            table.heading("#" + str(i), text = labels[i], anchor = tkinter.W)
        for item in allItems:
            valueA = "X" if item in listA else ""
            valueB = "X" if item in listB else ""
            table.insert("", "end", text = item, values=(valueA, valueB))
        table.pack(side = tkinter.TOP, fill = tkinter.X)
        self.showSaveAsCsvFileButtonForTables(window, table, labels)
     
    """
    this function creates a tkinter treeview with a table like look inserts the
    key value pairs of a dict with lists as values
    """        
    def createTableFromDictWithListsAsValue(self, window, labels,  dictionary, limit):
        table = ttk.Treeview(window)
        table["columns"] = tuple("#" + str(i) for i in range(1, len(labels)))
        for i in range(len(labels)):
            table.column("#" + str(i), width=400, minwidth=200)
        for i in range(len(labels)):
            table.heading("#" + str(i), text = labels[i], anchor = tkinter.W)
        ttk.Style().configure("Treeview", rowheight = 5 * limit)
        for key in dictionary.keys():
            value = "No Hashtags found in witheld Posts"
            if dictionary[key]:
                value = ""
                tempList = list(set(dictionary[key]))[:limit]
                for i in range(len(tempList)):
                    if ((i % 3 == 0) and (i != 0)):
                        value += '\n'
                    value += tempList[i] + ", "
            table.insert("", "end", text = key, values=(value,))
        table.pack(side = tkinter.TOP, fill = tkinter.X)
        self.showSaveAsCsvFileButtonForTables(window, table, labels)
        
    """
    this function creates the error message window
    """
    def createErrorMessageWindow(self, window, errorList):
        errorMessages = self.userInputfFieldsErrorCodeErrorMessageMapper()
        errorWindow = tkinter.Toplevel(window)
        errorWindow.wm_title("Error Message Window")
        for key in errorList:
            message = tkinter.Label(errorWindow, text = errorMessages[key])
            message.pack()
            
    """
    this function is used when the user clicked on the forward button 
    in the histogram slideshow and selects the next diagram in
    the list
    """        
    def callBackButtonForwardSlideShow(self, window, fig, counter):
        if counter != len(fig):
            counter += 1
            self.deleteAllWidgetsOfAWindow(window)
            self.createSlideShowCanvas(window, fig[counter])
            self.createSlideShowButtons(window, fig)
    
    """
    this function is used when the user clicked on the backward button 
    in the histogram slideshow and selects the previous diagram in
    the list
    """               
    def callBackButtonBackwardSlideShow(self, window, fig, counter):
        if counter >= 0:
            if counter > 0:
                counter -= 1
            self.deleteAllWidgetsOfAWindow(window)
            self.createSlideShowCanvas(window, fig[counter])
            self.createSlideShowButtons(window, fig)
            
    """
    this function is draws a diagram for the slideshow and makes it
    visible for the user
    """               
    def createSlideShowCanvas(self, window, figure):
        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1) 
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
    """
    this function creates the buttons for the histogram slideshow
    """       
    def createSlideShowButtons(self, window, figures):
            buttonForward = tkinter.Button(master=window, text="Forward", 
                                    command = lambda window = window, 
                                    fig = figures, counter = self.slideShowCounter: 
                                        self.callBackButtonForwardSlideShow(window, fig, counter))
            buttonForward.pack(side=tkinter.RIGHT)
            buttonBackward = tkinter.Button(master=window, text="Backward", 
                                    command = lambda window = window, 
                                    fig = figures, counter = self.slideShowCounter: 
                                        self.callBackButtonBackwardSlideShow(window, fig, counter))
            buttonBackward.pack(side=tkinter.LEFT)
            
    """
    this function creates the histogram slideshow  for a specifuc headline
    """        
    def createSlideShowOfHistograms(self, args):
        limit = int(args[3].get())
        dateFormat = self.getDateFormats()[args[1]]
        date = self.filterObject.convertInputDateToUsableDate(args[2].get(), 
                                                                  dateFormat[0],
                                                                  dateFormat[1])
        labels = self.getAxisLabelsForSlidesShow(date)[args[1]]
        year = (args[2].get().split("/")[2] if dateFormat == ['%d/%m/%Y', '%b %d'] 
                    else args[2].get().split("/")[1])
        reversing = True if args[-1].get() == 1 else False
        print(date)
        result = self.getOnehistogramFunctioAndOneParameternMapper()[args[1]](date, year)
        print("result")
        figures = self.getFiguresForSlideShowFromDictAsList(result, limit, reversing, labels)
        newWindow = tkinter.Toplevel(args[0])
        newWindow.geometry("500x500")
        self.createSlideShowCanvas(newWindow, figures[0])
        self.createSlideShowButtons(newWindow, figures)
    
    """
    this function calls and shows the user input fields
    """
    def showUserInputFields(self, window, comboBox):
        userChosed = comboBox.get()
        radioButtonChoses = [("Descending", 1), ("Ascending", 2)]
        entryFieldDate = self.textInputCombinationField(window, "Date", 1)
        buttonRow, fieldRow, radioRow = 4, 2, 3
        argsList = [window, userChosed, entryFieldDate]
        if userChosed == "Analysis of the difference in two dates":
                buttonRow, fieldRow, radioRow = 5, 3, 4
                entryFieldSecondDate = self.textInputCombinationField(window, "Second Date", 2)
                argsList.append(entryFieldSecondDate)
        entryFieldLimit = self.textInputCombinationField(window, "Display Limit", fieldRow)
        argsList.append(entryFieldLimit)
        radioButtonChoseGetter = self.createRadioButtonWithLabel(window, radioButtonChoses, "Sorting", radioRow)
        argsList.append(radioButtonChoseGetter)
        button = tkinter.Button(window, text='Start Analysis', width=25, 
                            command = lambda args = argsList: self.callBackButton(args))
        button.grid(row=buttonRow)
        
    """
    a function for creating the the user input fields based on the chose
    of the comBox field
    """
    def CallBackForComboBox(self, event, window, comboBox):
        self.setRootWindowToInitalState(window)
        if comboBox.get() != "Please choose an analysis Type:":
            self.showUserInputFields(window, comboBox)
            
    """
    this function creates adn show the compare table to the user
    """    
    def showCompareTable(self, args):
        limit = int(args[3].get())
        dateFormat = self.getDateFormats()[args[1]]
        columnLabels = self.getLabelsForCompareTable()[args[1]]
        date = self.filterObject.convertInputDateToUsableDate(args[2].get(), 
                                                                  dateFormat[0],
                                                                  dateFormat[1])
        year = (args[2].get().split("/")[2] if dateFormat == ['%d/%m/%Y', '%b %d'] 
                    else args[2].get().split("/")[1])
        print(date)
        resultA, resultB = self.getFunctionsThatWillBeShownASCompareTable()[args[1]](date, year)
        print("result")
        newWindow = tkinter.Toplevel(args[0])
        self.createCompareTable(newWindow, columnLabels, resultA[:limit], resultB[:limit])
    
    """
    this function creates and shows the table for listing dicts
    """    
    def showTableOfADictWithLists(self, args):
         limit = int(args[3].get())
         dateFormat = self.getDateFormats()[args[1]]
         columnLabels = self.getLabelsForCompareTable()[args[1]]
         date = self.filterObject.convertInputDateToUsableDate(args[2].get(), 
                                                               dateFormat[0],
                                                               dateFormat[1])
         year = (args[2].get().split("/")[2] if dateFormat == ['%d/%m/%Y', '%b %d'] 
                 else args[2].get().split("/")[1])
         print(date)
         result = self.getFunctionsThatWillBeShownASCompareTable()[args[1]](date, year)
         print("result")
         newWindow = tkinter.Toplevel(args[0])
         self.createTableFromDictWithListsAsValue(newWindow, columnLabels, result, limit)
    
    """
    this function creates the gui elements for an analysis with 3 parameters
    """ 
    def showCompareTableWithThreeParameterFunctions(self, args):
        limit = int(args[4].get())
        dateFormat = self.getDateFormats()[args[1]]
        columnLabels = self.getLabelsForCompareTable()[args[1]]
        dateA = self.filterObject.convertInputDateToUsableDate(args[2].get(), 
                                                               dateFormat[0],
                                                               dateFormat[1])
        dateB = self.filterObject.convertInputDateToUsableDate(args[3].get(), 
                                                               dateFormat[0],
                                                               dateFormat[1])
        yearA = (args[2].get().split("/")[2] if dateFormat == ['%d/%m/%Y', '%b %d'] 
                 else args[2].get().split("/")[1])
        yearB = (args[3].get().split("/")[2] if dateFormat == ['%d/%m/%Y', '%b %d'] 
                 else args[3].get().split("/")[1])
        print(dateA, dateB)
        resultA, resultB = self.getFunctionsThatWillBeShownASCompareTable()[args[1]](dateA, dateB, yearA, yearB)
        print("result")
        newWindow = tkinter.Toplevel(args[0])
        self.createCompareTable(newWindow, columnLabels, resultA[:limit], resultB[:limit])
        
    """
    this function gets the ersult of each specific analysis that will be shown
    as a histogram later on
    """    
    def getResultForHistogram(self, args, date, year):
        result = (self.filterObject.sortDictionary(
                 self.getOnehistogramFunctioAndOneParameternMapper()[args[1]](date,year),
                 True if args[-1].get() == 1 else False) if args[1] not in 
                 list(self.getOnehistogramFunctioAndTwoParameternMapper().keys()) 
                 else self.filterObject.sortDictionary(
                     self.getOnehistogramFunctioAndTwoParameternMapper()[args[1]](date,
                 self.getOnehistogramFunctioAndTwoParameternCounterMapper()[args[1]], 
                 "DESC" if args[-1].get() == 1 else "ASC", year), True if args[-1].get() == 1 else False))
        return result
    
    """
    this function gets the key value pairs in a range of the limit parameter
    """    
    def getKeyValuePairsOfDictWithLimitation(self, result, limit):
        counter = 0
        keys, values = list(), list()
        for key in result.keys():
            if counter == limit:
                break
            keys.append(key)
            values.append(result[key])
            counter += 1   
        return keys, values
    
    """
    this function creates a singel histogram and will be shown in the gui
    """    
    def showHistogram(self, args):
        limit = int(args[3].get())
        dateFormat = self.getDateFormats()[args[1]]
        date = self.filterObject.convertInputDateToUsableDate(args[2].get(), 
                                                              dateFormat[0],
                                                              dateFormat[1])
        labels = self.getLabelForHistograms(date)[args[1]]
        year = (args[2].get().split("/")[2] if dateFormat == ['%d/%m/%Y', '%b %d'] 
                else args[2].get().split("/")[1])
        print(date)
        result = self.getResultForHistogram(args, date, year)
        print("result")
        keys, values = self.getKeyValuePairsOfDictWithLimitation(result, limit)
        newWindow = tkinter.Toplevel(args[0])
        newWindow.geometry("500x500")
        self.drawHistogram(newWindow, keys, values, labels)
    
    """
    a function for executing the specific analysis and showing it in a
    new window
    """        
    def callBackButton(self, args):
        errorList = self.ckeckUserInputFielsForErrors(args)
        if errorList:
            self.createErrorMessageWindow(args[0], errorList)
        elif args[1] == "Frequency Analysis sorted by Country (Specific Date)":
            self.slideShowCounter = 0
            self.createSlideShowOfHistograms(args)
        elif ((args[1] in list(self.getOnehistogramFunctioAndOneParameternMapper().keys())) or 
        (args[1] in list(self.getOnehistogramFunctioAndTwoParameternCounterMapper().keys()))):
            self.showHistogram(args)
        elif args[1] == "Analysis of the difference in two dates":
            self.showCompareTableWithThreeParameterFunctions(args)
        elif args[1] == "Analysis Of Hashtags witheld by Country (Specific Date)":
            self.showTableOfADictWithLists(args)
        elif args[1] in list(self.getFunctionsThatWillBeShownASCompareTable().keys()):
            self.showCompareTable(args)
                
    # function for creating the comboBox        
    def createCreateComboBox(self):
        labelsToChoose = self.getListOfHeadlinesOFallAnalyze()
        comboBox = ttk.Combobox(self.rootWindow, state = "readonly", 
                                values = labelsToChoose, width = 75)
        comboBox.grid(column=0, row=0)
        comboBox.current(0)
        comboBox.bind("<<ComboboxSelected>>", lambda event: 
                      self.CallBackForComboBox(event, self.rootWindow, comboBox))
    
    """
    a function for getting a subplot histogram as figure to show it in tkinter
    """     
    def getHistogramFigureSubPlot(self, xAx, yAx, labels, colors):
        fig = Figure(figsize=(5, 4), dpi=100)
        diagram = fig.add_subplot(111)
        diagram.bar(xAx, yAx, color = colors)
        for tick in diagram.get_xticklabels():
            tick.set_rotation(45)
            tick.set_fontsize(10) 
        diagram.set_title(labels[0])
        diagram.set_xlabel(labels[1])
        diagram.set_ylabel(labels[2])
        return fig
    
    """
    a function for drawing the histogram and add it to a tkinter window
    """  
    def drawHistogram(self, window, xAx, yAx, labels = ["", "", ""], colors = None):
        fig = self.getHistogramFigureSubPlot(xAx, yAx, labels, colors)
        canvas = FigureCanvasTkAgg(fig, master = window) 
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        canvas.mpl_connect("key_press_event", self.on_key_press)
