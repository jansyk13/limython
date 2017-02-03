import logging as log
import numpy as np
import sys
import unittest
import transformation.url as url

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class UrlTest(unittest.TestCase):

    def testParser(self):
        urls = ['A/B/C', 'A/B/D']
        parser = url.MatrixUrlParser()

        result = parser.parse(urls)

        self.assertTrue(np.array_equal(result, [[1, 1, 1, 0], [1, 1, 0, 1]]),
                        'Matrixes not equals, result=%s' % result)

    def testRemovingRequestParams(self):
        urls = ['A/B?troll']
        parser = url.MatrixUrlParser()

        result = parser.parse(urls)

        self.assertTrue(np.array_equal(
            result, [[1, 1]]), 'Incorrectly parsed with params')

    def testDeduplicateListKeepingOrder(self):
        result = url.deduplicate(['A', 'B', 'A'])

        self.assertEqual(result, ['A', 'B'])
