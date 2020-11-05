import py_files.filesystemhandler as fsh
import py_files.crawler as cwl
import py_files.preprocessor as pre
import py_files.pearson as pear


class ControlManager:
    def __init__(self, query):
        self.query = query
        self.filterObject = None
        self.crawlerObject = None
        self.fileHandler = fsh.FileSystemHandler()

    def initSession(self):
        self.fileHandler.createRootDirectory()

    def closeSession(self):
        rootD = self.fileHandler.getRootDirectory()
        self.fileHandler.deleteSessionTempFiles(rootD)

    def crawlQuery(self):
        self.crawlerObject = cwl.Crawler(self.query)
        lib = self.crawlerObject.getLibUrl()
        if lib is not None:
            text = self.crawlerObject.getTextFromWebsite(lib)
            self.crawlerObject.writeTextToFile(text)
            return False
        return True

    def executeFiltering(self):
        file = self.fileHandler.getSearchFilePath(self.query.split(":")[0],
                                                  self.query.split(":")[1] +
                                                  ".txt")
        searchString = self.query.split(":")[2]
        preprocessor = pre.Preprocessor(file, searchString)
        tfidfMatrix = preprocessor.vectoriseData()
        linesToPickRelevantLinesFrom = preprocessor.getLinesWithoutEmptyLines()
        pearson = pear.Pearson(tfidfMatrix, linesToPickRelevantLinesFrom)
        return pearson.generateResponse()
