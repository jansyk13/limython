import logging as log
import pandas as pd
import numpy as np
import numpy.testing as npt
import sys
import unittest
import validation.kfold as kfold
import learning.ols as ols

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestKfold(unittest.TestCase):

    def testValidate(self):
        df = pd.DataFrame({"A": [10, 20, 30, 40, 50], "B": [
                           20, 30, 10, 40, 50], "payload_size": [32, 234, 23, 23, 42523]})
        validator = kfold.Kfold(_help, df, ['A', 'B'], 2, {})
        validator.validate(True)

    def testGroups(self):
        groups = kfold._groups(5, 11)

        npt.assert_allclose(groups, np.array(
            [0., 0., 1., 1., 2., 2., 3., 3., 4., 4., 0.]))


def _help(args):
    return ols.Ols()
