import io
import os
import sys
import random
import string
import warnings
import numpy as np
import warnings
import nltk
from nltk.stem import WordNetLemmatizer
import re
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline, FeatureUnion


class Preprocessor:
    def __init__(self, dataFolderPath, userInput):
        self.dataFolderPath = dataFolderPath
        self.userInput = userInput
        self.lines = self.fetchData().split('\n')

    def getIndexOfEmptyLines(self):
        textWithoutUserInput = self.stemming()[:-1]
        return [index for index in range(len(textWithoutUserInput))
                if textWithoutUserInput[index] == '']

    def getLinesWithoutEmptyLines(self):
        text = self.removeDuplicateLines()
        indexOfEmptyLines = self.getIndexOfEmptyLines()
        for index in indexOfEmptyLines:
            del text[index]
        return text

    def vectoriseData(self):
        vectorizer = Pipeline([('vectorizer', CountVectorizer()),
                              ('tfidf', TfidfTransformer())])
        X = vectorizer.fit_transform(self.removeEmptyLines(self.stemming()))
        return X

    def removeEmptyLines(self, text):
        return [line for line in text if line is not '']

    def stemming(self):
        words = str()
        stemmedWords = list()
        st = PorterStemmer()
        for line in self.meaningfulWords():
            words = ''
            for w in line.split():
                words += st.stem(w) + ' '
            stemmedWords.append(words.strip())
        return stemmedWords

    def meaningfulWords(self):
        meaningfulWords = []
        words = str()
        tags = ['VB', 'VBP', 'VBD', 'VBG',
                'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS',
                'NN', 'NNS', 'NNP', 'NNPS', 'CD']
        text = self.negationHandling()
        for line in text:
            taggedWord = pos_tag(line.split())
            words = ''
            for w in taggedWord:
                if w[1] in tags:
                    words += w[0] + ' '
            meaningfulWords.append(words.strip())
        return meaningfulWords

    def negationHandling(self):
        counter = False
        modNegations = []
        words = str()
        negations = ['no', 'not', 'cant', 'cannot', 'never', 'less', 'without',
                     'barely', 'hardly', 'rarely', 'noway', 'didnt']
        text = self.removeStopWords()
        for line in text:
            words = ''
            for i, j in enumerate(line.split()):
                if j in negations and i < len(line.split())-1:
                    words += str(line.split()[i]+'-'+line.split()[i+1]) + ' '
                    counter = True
                else:
                    if counter is False:
                        words += line.split()[i] + ' '
                    else:
                        counter = False
            modNegations.append(words.strip())
        return modNegations

    def removeStopWords(self):
        stop = set(stopwords.words('english'))
        stop.update(['compute', 'calculate', 'get', 'use'])
        words = str()
        noStops = list()
        for line in self.removePunctuations():
            words = ''
            for w in line.split():
                if w not in stop:
                    words += w + ' '
            noStops.append(words.strip())
        return noStops

    def removePunctuations(self):
        words = str()
        noPunctuations = list()
        text = self.appendLoweredUserInput()
        for line in text:
            words = ''
            for w in re.sub(r'[^\w\s]', '', line).split():
                words += w + ' '
            noPunctuations.append(words.strip())
        return noPunctuations

    def appendLoweredUserInput(self):
        textWithUserInput = self.removeDuplicateLines()
        textWithUserInput.append(self.userInput.lower())
        return textWithUserInput

    def removeDuplicateLines(self):
        lines = self.removeBlanks()
        return list(dict.fromkeys(lines))

    def removeBlanks(self):
        lines = self.getParagraphs()
        return list(filter(None, lines))

    def getParagraphs(self):
        text = self.fetchData().split('\n')
        groupedByParagraphsText = self.groupTextByParagraphs().split('\n')
        if not self.enoughParagraphs():
            return text
        else:
            return groupedByParagraphsText

    def enoughParagraphs(self):
        count = 0
        minNumOfParagrpahs = 5
        for line in self.lines:
            if line == '':
                count += 1
        if count <= minNumOfParagrpahs:
            return False
        else:
            return True

    def groupTextByParagraphs(self):
        temp = str()
        groupedByParagraphsText = str()
        for line in self.lines:
            if line is not '':
                temp += line.strip() + ' '
            elif line == '' and temp != '':
                groupedByParagraphsText += temp.strip() + '\n'
                temp = ''
        if temp != '':
            groupedByParagraphsText += temp.strip()
        return groupedByParagraphsText

    def fetchData(self):
        rawData = str()
        with open(self.dataFolderPath, 'r', encoding='utf8',
                  errors='ignore') as f:
            rawData += f.read().lower()
        return rawData
