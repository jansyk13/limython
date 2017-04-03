import logging as log
import pandas as pd
import numpy as np
import numpy.testing as npt
import sys
import unittest
import learning.tree as tree

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestTree(unittest.TestCase):

    def testLearning(self):
        ldf = pd.DataFrame({"A": [10, 20, 30, 40, 50], "B": [
                           20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})

        model = tree.Tree('min_samples_leaf=1')
        model.learn(y=ldf['C'], x=ldf[['A', 'B']])

    def testPredict(self):
        ldf = pd.DataFrame({"A": [10, 20, 30, 40, 50], "B": [
                           20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})
        pdf = pd.DataFrame(
            {"A": [10, 20, 30, 40, 50], "B": [20, 30, 10, 40, 50]})

        model = tree.Tree('min_samples_leaf=1')
        model.learn(y=ldf['C'], x=ldf[['A', 'B']])

        result = model.predict(pdf)

        expected = np.array([3.200000e+01, 2.340000e+02, 2.300000e+01, 2.300000e+01, 4.252300e+04])
        npt.assert_allclose(result, expected)
