import numpy as np
from scipy.stats import pearsonr
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity


class Pearson:
    def __init__(self, tfidfMatrix, sentences):
        self.tfidfMatrix = tfidfMatrix
        self.pearsonCoeffs = self.getPearsonCoeffsOfUserInputAndData()
        self.sentences = sentences

    def generateResponse(self):
        response = str()
        topKMatches = 4
        indexTopKSentences = self.getIndexOfTopKMatches(topKMatches)

        if(self.correlationMatch()):
            for i in range(len(indexTopKSentences)-1, -1, -1):
                response += self.sentences[indexTopKSentences[i]]+"\n\n"
            return response
        else:
            response += "Sorry dont know about that one"
            return response

    def correlationMatch(self):
        highestCorrelation = np.sort(self.pearsonCoeffs)[-1]
        if(highestCorrelation <= 0):
            return False
        else:
            return True

    def tooManyChars(self, text):
        charLimit = 2000
        if len(text) > charLimit:
            return True
        else:
            return False

    def getIndexOfTopKMatches(self, k):
        indexTopKSentences = np.asarray(self.pearsonCoeffs)
        return [index for index in indexTopKSentences.argsort()
                if not self.tooManyChars(self.sentences[index])][-k:]

    def getPearsonCoeffsOfUserInputAndData(self):
        coeff = list()
        userInput = self.tfidfMatrix.toarray()[-1]
        tfidfWithOutUserInput = self.tfidfMatrix[:-1]
        for row in tfidfWithOutUserInput:
            if np.std(row.getrow(0).toarray()[0]) != 0:
                row = row.getrow(0).toarray()[0]
                coeff.append((pearsonr(userInput, row))[0])
            else:
                coeff.append(0)
        return coeff
