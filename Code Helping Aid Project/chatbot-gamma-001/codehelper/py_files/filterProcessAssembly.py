import py_files.preprocessor as pre
import py_files.pearson as pear
import py_files.kmeans as kmeans
import os


class FilterProcessAssembly:
    def __init__(self, filePath, searchString):
        self.filePath = filePath
        self.searchString = searchString
        self.preprocessor = None

    def initialisePreprocesser(self, filePath):
        self.preprocessor = pre.Preprocessor(filePath, self.searchString)

    def getPreprocessedPath(self):
        if os.name == 'posix':
            return '/'.join(self.filePath.split('/')[:-1])+'/preprocessed.txt'
        return '\\'.join(self.filePath.split('\\')[:-1])+'\\preprocessed.txt'

    def getTfidifMatrix(self):
        return self.preprocessor.vectoriseData()

    def getUnfilteredSentences(self):
        return self.preprocessor.removeDuplicateLines()

    def dropResultsWithTooManyChars(self, text):
        charLimit = 1000
        return '\n'.join([x for x in text.split('\n')
                         if len(x) <= charLimit])

    def writeToFile(self, data):
        with open(self.getPreprocessedPath(), "w", encoding="utf8") as f:
            f.write(data)

    def assembleFilterPipe(self):
        self.initialisePreprocesser(self.filePath)
        p = pear.Pearson(self.getTfidifMatrix(), self.getUnfilteredSentences())
        self.writeToFile(self.dropResultsWithTooManyChars(p
                                                          .generateResponse()))
        self.initialisePreprocesser(self.getPreprocessedPath())
        k = kmeans.Kmeans(self.getTfidifMatrix(),
                          self.getUnfilteredSentences())
        return k
