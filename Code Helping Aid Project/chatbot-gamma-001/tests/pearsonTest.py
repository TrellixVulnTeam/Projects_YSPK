import sys
import unittest
import py_files.pearson as p
import py_files.preprocessor as pre
sys.path.append('..')


class pearsonTest(unittest.TestCase):
    query = 'how to compute base 10 logarithm'
    path = '../tests/data/math/numpyMathFunctions.txt'
    preprocessor = pre.Preprocessor(path, query)
    X = preprocessor.vectoriseData()
    sentences = preprocessor.removeDuplicateLines()
    pearson = p.Pearson(X, sentences)

    def testInit(self):
        self.assertIsNotNone(self.pearson.tfidfMatrix)
        self.assertIsNotNone(self.pearson.pearsonCoeffs)
        self.assertIsNotNone(self.pearson.sentences)
        lenPearson = len(self.pearson.sentences)
        self.assertEqual(self.pearson.tfidfMatrix[:-1].shape[0], lenPearson)

    def testGetPearsonCoeffsOfUserInputAndData(self):
        self.assertIsNotNone(self.pearson.getPearsonCoeffsOfUserInputAndData())
        lenPearson = len(self.pearson.getPearsonCoeffsOfUserInputAndData())
        self.assertEqual(self.pearson.tfidfMatrix[:-1].shape[0], lenPearson)

    def testGetIndexOfTopKMatches(self):
        topKMatches = 3
        index = self.pearson.getIndexOfTopKMatches(topKMatches)
        self.assertIsNotNone(index)
        self.assertEqual(len(index), topKMatches)

    def testTooManyChars(self):
        textShort = ''.join(['a' for c in range(2000)])
        textLong = ''.join(['a' for c in range(2001)])
        self.assertIsNotNone(self.pearson.tooManyChars(textShort))
        self.assertIsNotNone(self.pearson.tooManyChars(textLong))
        self.assertTrue(self.pearson.tooManyChars(textLong))
        self.assertFalse(self.pearson.tooManyChars(textShort))

    def testGenerateResponse(self):
        self.assertIsNotNone(self.pearson.generateResponse())


if __name__ == '__main__':
    unittest.main()
