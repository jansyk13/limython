import logging as log
import numpy as np
import processors.simple_processor as sp
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestSimpleRoundRobinProcessor(unittest.TestCase):

    def testProcess(self):
        predictions = np.array([1, 10, 10, 1, 10])
        p = sp.SimpleRoundRobinProcessor(3)

        for idx, prediction in np.ndenumerate(predictions):
            p.process(prediction)

        self.assertListEqual(p.node_counters, [2, 20, 10])
