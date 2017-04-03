import logging as log
import pandas as pd
import numpy as np
import numpy.testing as npt
import sys
import unittest
import learning.sgd as sgd

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestSgd(unittest.TestCase):

    def testLearning(self):
        ldf = pd.DataFrame({"A": [10, 20, 30, 40, 50], "B": [
                           20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})

        model = sgd.Sgd('alpha=0.00001')
        model.learn(y=ldf['C'], x=ldf[['A', 'B']])

    def testPredict(self):
        ldf = pd.DataFrame({"A": [10, 20, 30, 40, 50], "B": [
                           20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})
        pdf = pd.DataFrame(
            {"A": [10, 20, 30, 40, 50], "B": [20, 30, 10, 40, 50]})

        model = sgd.Sgd('alpha=0.00001')
        model.learn(y=ldf['C'], x=ldf[['A', 'B']])

        model.predict(pdf)
        # cannot be asserted
