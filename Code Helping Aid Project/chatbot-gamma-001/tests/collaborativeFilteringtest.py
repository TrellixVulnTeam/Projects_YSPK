import sys
import unittest
import py_files.collaborativeFiltering as cf
import numpy as np
sys.path.append('..')


class collaborativeFilteringtest(unittest.TestCase):

    query = 'python:math: how to use cosine'
    filter = cf.CollaborativeFiltering('data/', query)

    def testInit(self):
        query = 'python:math: how to use cosine'
        self.assertEqual(self.filter.dataFolderPath, 'data/')
        self.assertEqual(self.filter.user_input, query)
        self.assertIsNotNone(self.filter.sentences_tokens)

    def testFetchData(self):
        self.assertIsNotNone(self.filter.fetchData())
        self.assertIn(self.filter.sentences_tokens[0], self.filter.fetchData())

    def testBuildSentencesTokens(self):
        self.assertIsNotNone(self.filter.buildSentencesTokens())
        self.assertIsInstance(self.filter.buildSentencesTokens(), list)

    def testLemmatiseTokens(self):
        sentenceTokens = self.filter.sentences_tokens
        self.assertIsNotNone(self.filter.lemmatiseTokens(sentenceTokens))

    def testNormaliseLemmatisedTokens(self):
        data = self.filter.fetchData()
        normaliseLemmatisedToken = self.filter.normaliseLemmatisedTokens(data)
        lower = normaliseLemmatisedToken[0].lower()
        self.assertIsNotNone(normaliseLemmatisedToken)
        self.assertNotIn(normaliseLemmatisedToken[0], '.')
        self.assertEqual(normaliseLemmatisedToken[0], lower)

    def testVectoriseData(self):
        data = self.filter.vectoriseData()
        self.assertIsNotNone(data)
        self.assertEqual(data.shape[0], len(self.filter.sentences_tokens)+1)

    def testPearsonCoeffs(self):
        p = self.filter.vectoriseData()[-1]
        self.assertEqual(self.filter.pearson_coeffs(p, p)[0], 1.0)

    def testGetPearsonSimOfUserInputAndData(self):
        numA = len(self.filter.sentences_tokens)+1
        numB = len(self.filter.getPearsonSimOfUserInputAndData())
        self.assertEqual(numA, numB)

    def testCorrelationMatch(self):
        self.assertFalse(self.filter.correlationMatch(np.array([0, 1])))
        self.assertTrue(self.filter.correlationMatch(np.array([1, 2])))

    def testGetIndexOfTopKMatches(self):
        data = self.filter.getPearsonSimOfUserInputAndData(),
        index = self.filter.getIndexOfTopKMatches(data, 1)
        self.assertIsNotNone(index)
        self.assertEqual(len(index), 1)
        self.assertIsInstance(index, np.ndarray)

    def testGenerateResponse(self):
        self.assertEqual(self.filter.generateResponse()[0:3], 'cos')
        self.assertIsNotNone(self.filter.generateResponse())


if __name__ == '__main__':
    unittest.main()
