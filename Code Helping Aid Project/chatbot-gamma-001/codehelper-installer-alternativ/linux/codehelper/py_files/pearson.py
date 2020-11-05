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
        topKMatches = 20
        indexTopKSentences = self.getIndexOfTopKMatches(topKMatches)

        if(self.correlationMatch()):
            for i in range(indexTopKSentences.size-1, -1, -1):
                response += self.sentences[indexTopKSentences[i]]+"\n"
            return response
        else:
            response += "Sorry dont know about that one"
            return response

    def correlationMatch(self):
        highestCorrelation = np.sort(self.pearsonCoeffs)[-2]
        if(highestCorrelation <= 0):
            return False
        else:
            return True

    def getIndexOfTopKMatches(self, k):
        indexTopKSentences = np.asarray(self.pearsonCoeffs)
        indexTopKSentences = indexTopKSentences.argsort()[-(k+1):-1]
        return indexTopKSentences

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
