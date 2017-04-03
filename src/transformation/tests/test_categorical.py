
import numpy.testing as npt
import logging as log
import pandas as pd
import sys
import unittest
import transformation.categorical as categorical

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestCategorical(unittest.TestCase):

    def test(self):
        df = pd.DataFrame(
            {
                "A": ["a", "b", "c", "a"],
                "B": ["a", "b", "c", "a"],
                "C": [1, 0, 1, 0],
                "D": [1, 0, 1, 0]
            }
        )
        df['A'] = df['A'].astype('category')
        df['B'] = df['B'].astype('category')

        tdf, headers = categorical.tranform(df, "D")

        edf = pd.DataFrame(
            {
                "A/a": [1, 0, 0, 1], "A/b": [0, 1, 0, 0], "A/c": [0, 0, 1, 0],
                "B/a": [1, 0, 0, 1], "B/b": [0, 1, 0, 0], "B/c": [0, 0, 1, 0],
                "C": [1, 0, 1, 0],
                "D": [1, 0, 1, 0]
            }
        )

        npt.assert_allclose(tdf.sort(axis=1), edf.sort(axis=1))
        self.assertEqual(headers, ['C', 'A/a', 'A/b', 'A/c', 'B/a', 'B/b', 'B/c'])
