import logging as log
import numpy as np
import processors.best_counter_processor as bp
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestDummyProcessor(unittest.TestCase):

    def testProcess(self):
        data = np.array([1, 10, 10, 1, 10])
        p = bp.BestCounterProcessor(3)

        for idx, prediction in np.ndenumerate(data):
            p.process(prediction, prediction)

        self.assertListEqual(p.real_node_counters, [12, 10, 10])
        self.assertListEqual(p.predict_node_counters, [12, 10, 10])
