from models.request import Request
import transformation.data as data
import logging as log
import numpy as np
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class DataTest(unittest.TestCase):

    def testData(self):
        req1 = Request(1, '127.0.0.1', '30:13:57:47',
                       'GET', 'A/B/C', 'HTTP 1.1', 200, 200)
        req2 = Request(1, '127.0.0.1', '30:13:57:47',
                       'POST', 'A/B/D', 'HTTP 1.1', 204, -1)
        requests = [req1, req2]

        matrix, payloads, labels = data.transform(requests)

        self.assertEqual(np.array_equal(
            matrix, [[1, 1], [1, 0], [0, 1], [1, 1], [0, 1], [1, 0], [1, 0], [0, 1]]))
        self.assertEqual(np.array_equal(
            payloads, [200, -1]), 'Payloads not equal')
        self.assertEqual(np.array_equal(labels, [
                         '127.0.0.1', 'GET', 'POST', 'HTTP 1.1', 200, 204, 'A/B/C', 'A/B/D']), 'Labels not equal')
        log.info('action=trrrrrrrrrrrollll  %s %s %s' %
                 (matrix, payloads, labels))
