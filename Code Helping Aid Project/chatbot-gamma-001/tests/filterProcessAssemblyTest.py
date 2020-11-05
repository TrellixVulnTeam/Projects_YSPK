import sys
import os
import unittest
import numpy as np
import py_files.preprocessor as pre
import py_files.pearson as pear
import py_files.kmeans as kmeans
import py_files.filterProcessAssembly as fpa
sys.path.append('..')


class FilterProcessAssemblyTest(unittest.TestCase):
    filePath = '..\\tests\\data\\math\\numpyMathFunctions.txt'
    searchString = 'how to compute cosine'
    fassembly = fpa.FilterProcessAssembly(filePath, searchString)

    def testInit(self):
        self.assertIsNotNone(self.fassembly.filePath)
        self.assertIsNotNone(self.fassembly.searchString)

    def testInitiaslisePreprocessor(self):
        self.assertTrue(isinstance(self.fassembly.preprocessor,
                                   pre.Preprocessor))

    def testGetPreprocessedPath(self):
        path = str()
        if os.name == 'posix':
            path = '/'.join(self.filePath.split('/')[:-1])+'/preprocessed.txt'
        else:
            path = '\\'\
                    .join(self.filePath.split('\\')[:-1])+'\\preprocessed.txt'
        self.assertEqual(self.fassembly.getPreprocessedPath(), path)

    def testGetTfidfMatrix(self):
        self.fassembly.initialisePreprocesser(self.filePath)
        self.assertIsNotNone(self.fassembly.getTfidifMatrix())

    def testGetUnfilteredSenctences(self):
        self.assertIsNotNone(self.fassembly.getUnfilteredSentences())
        self.assertTrue(isinstance(self.fassembly.getUnfilteredSentences()[0],
                        str))

    def testDropResultsWithTooManyChars(self):
        self.fassembly.initialisePreprocesser(self.filePath)
        X = self.fassembly.getTfidifMatrix()
        sentences = self.fassembly.getUnfilteredSentences()
        p = pear.Pearson(X, sentences)
        text = self.fassembly.dropResultsWithTooManyChars(p.generateResponse())
        for line in text:
            self.assertLessEqual(len(line), 1000)

    def testWriteToFile(self):
        self.fassembly.initialisePreprocesser(self.filePath)
        X = self.fassembly.getTfidifMatrix()
        sentences = self.fassembly.getUnfilteredSentences()
        p = pear.Pearson(X, sentences)
        text = self.fassembly.dropResultsWithTooManyChars(p.generateResponse())
        path = self.fassembly.getPreprocessedPath()
        self.fassembly.writeToFile(text)
        with open(path, 'r', encoding='utf8', errors='ignore') as f:
            self.assertIsNotNone(f.read())

    def testAssembleFilterPipe(self):
        self.assertIsNotNone(self.fassembly.assembleFilterPipe().
                             generateResponse())
        self.assertTrue(isinstance(self.fassembly.assembleFilterPipe(),
                                   kmeans.Kmeans))


if __name__ == '__main__':
    unittest.main()
