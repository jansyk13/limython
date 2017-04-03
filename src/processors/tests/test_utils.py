import logging as log
import numpy as np
import pandas as pd
import sys
import unittest
import processors.utils as utils
import processors.dummy_processor as processor

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestUtils(unittest.TestCase):

    def testParse(self):
        df = pd.DataFrame({"payload_size": [10, 20, 30, 40, 50]})
        p = np.array([10, 20, 30, 40, 50])
        rmse, rsquarred = utils.process_and_compute_stats(
            processor.DummyProcessor(), df, p)

        self.assertEqual(rmse, 0)
        self.assertEqual(rsquarred, 1.0)
