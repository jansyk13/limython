import logging as log
import pandas as pd
import numpy as np
import numpy.testing as npt
import sys
import unittest
import validation.kfold_baseline as kfold
import learning.ols as ols
import processors.dummy_processor as dummy

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestKfold(unittest.TestCase):

    def testValidate(self):
        df = pd.DataFrame({"A": [10, 20, 30, 40, 50], "B": [
                           20, 30, 10, 40, 50], "payload_size": [32, 234, 23, 23, 42523]})
        validator = kfold.KfoldBaseline(_help_dummy, df, 2, {})
        validator.validate()


def _help_dummy(args):
    return dummy.DummyProcessor()
