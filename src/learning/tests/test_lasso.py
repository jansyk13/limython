import logging as log
import pandas as pd
import numpy as np
import numpy.testing as npt
import sys
import unittest
import learning.lasso as lasso

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestLasso(unittest.TestCase):

    def testLearning(self):
        ldf = pd.DataFrame({"A": [10, 20, 30, 40, 50], "B": [
                           20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})

        model = lasso.Lasso('')
        model.learn(y=ldf['C'], x=ldf[['A', 'B']])

    def testPredict(self):
        ldf = pd.DataFrame({"A": [10, 20, 30, 40, 50], "B": [
                           20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})
        pdf = pd.DataFrame(
            {"A": [10, 20, 30, 40, 50], "B": [20, 30, 10, 40, 50]})

        model = lasso.Lasso('')
        model.learn(y=ldf['C'], x=ldf[['A', 'B']])

        result = model.predict(pdf)

        expected = np.array(
            [-6375.455632, 3610.534129, -1492.04778, 18552.989761, 28538.979523])
        npt.assert_allclose(result, expected)
