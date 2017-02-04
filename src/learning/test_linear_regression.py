from models.request import Request
import learning.linear_regression as reg
import logging as log
import numpy as np
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class LinearRegressionTest(unittest.TestCase):

    def testJoing(self):
        a = np.array([[1, 1, 1]])
        b = np.array([[1, 1, 1]])

        result = np.concatenate((a, b), 0)

        self.assertTrue(np.array_equal(
            result, [[1, 1, 1], [1, 1, 1]]), 'a=%s b=%s result=%s' % (a, b, result))

    def testJoing2(self):
        a = np.empty((0, 3))
        b = np.array([[1, 1, 1]])

        result = np.concatenate((a, b), 0)

        self.assertTrue(np.array_equal(
            result, [[1, 1, 1]]), 'a=%s b=%s result=%s' % (a, b, result))

    def testTest(self):
        req1 = Request(1, '127.0.0.1', '30:13:57:47',
                       'GET', 'A/B/C', 'HTTP 1.1', 200, 200)
        requests = [req1]
        learning = reg.LinearRegression()

        learning.ws = np.array([[1], [1], [1], [1], [1], [1], [1]])
        learning.labels = ['127.0.0.1', 'GET',
                           'HTTP 1.1', 200, 'A', 'A/B', 'A/B/C']

        deviations, avg_dev = learning.test(requests)
        self.assertEqual(deviations, [3.5])
        self.assertEqual(avg_dev, 3.5)

    def testDescribe(self):
        req1 = Request(1, '127.0.0.1', '30:13:57:47',
                       'GET', 'A/B/C', 'HTTP 1.1', 200, 200)
        learning = reg.LinearRegression()

        learning.labels = ['127.0.0.1', 'GET',
                           'HTTP 1.1', 200, 'A', 'A/B', 'A/B/C']

        descriptor_matrix = learning._desribe(req1)
        self.assertTrue(np.array_equal(
            descriptor_matrix, [1, 1, 1, 1, 1, 1, 1]))
