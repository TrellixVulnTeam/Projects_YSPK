import numpy as np
from sklearn.cluster import KMeans
import sys

class Kmeans:
    def __init__(self, tfidfMatrix, sentences):
        self.tfidfMatrix = tfidfMatrix
        self.sentences = sentences

    def generateModel(self):
        kmeans = KMeans(n_clusters=int(len(self.sentences)/3))
        kmeans.fit_predict(self.tfidfMatrix)
        labels = kmeans.predict(self.tfidfMatrix)
        kmeans.cluster_centers_
        return labels

    def generateResponse(self):
        relevantSentences = str()
        labels = self.generateModel()
        idx = np.where(labels == labels[-1])
        for i in idx[0][:-1]:
            relevantSentences += self.sentences[int(i)] + '\n'
        if relevantSentences:
            return relevantSentences
        else:
            return "Sorry dont know about that one"
