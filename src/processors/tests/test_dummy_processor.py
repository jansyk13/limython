import logging as log
import numpy as np
import processors.dummy_processor as dp
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestDummyProcessor(unittest.TestCase):

    def testProcess(self):
        predictions = np.array([1, 10, 10, 1, 10])
        p = dp.DummyProcessor()

        for idx, prediction in np.ndenumerate(predictions):
            p.process(prediction)

        self.assertIsNone(p.node_counters)
