import logging as log
import pandas as pd
import numpy as np
import numpy.testing as npt
import sys
import unittest
import learning.ridge as ridge

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestRidge(unittest.TestCase):

    def testLearning(self):
        ldf = pd.DataFrame({"A": [10, 20, 30, 40, 50], "B": [
                           20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})

        model = ridge.Ridge('alpha=0.00001')
        model.learn(y=ldf['C'], x=ldf[['A', 'B']])

    def testPredict(self):
        ldf = pd.DataFrame({"A": [10, 20, 30, 40, 50], "B": [
                           20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})
        pdf = pd.DataFrame(
            {"A": [10, 20, 30, 40, 50], "B": [20, 30, 10, 40, 50]})

        model = ridge.Ridge('alpha=0.00001')
        model.learn(y=ldf['C'], x=ldf[['A', 'B']])

        result = model.predict(pdf)

        expected = np.array(
            [-6375.333246, 3610.666695, -1492.333272, 18552.999941, 28538.999883])

        npt.assert_allclose(result, expected)
