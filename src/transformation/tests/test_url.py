
import numpy.testing as npt
import logging as log
import pandas as pd
import sys
import unittest
import transformation.url as url

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestUrl(unittest.TestCase):

    def test_Parse(self):
        value = pd.DataFrame({"url": ["/A/B", "/A/B/C", "/A/B/C/D"]})

        result = url._parse(value)
        self.assertEqual(
            result, ['/A', '/A/B', '/A/B/C', '/A/B/C/D'])

    def testSplit(self):
        value = "/A/B/C/D"

        result = url._split(value)
        self.assertEqual(
            result, ['/A', '/A/B', '/A/B/C', '/A/B/C/D', '/A/B/C/D'])

    def testRemoveQueryParams(self):
        value = ["/A/B?test"]

        result = url._remove_query_params(value)
        self.assertEqual(result, ['/A/B'])

    def testDeduplicate(self):

        value = ['A', 'B', 'A']
        result = url._deduplicate(value)
        self.assertEqual(result, ['A', 'B'])
