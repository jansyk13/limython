import logging as log
import numpy as np
import processors.simple_processor as sp
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestSimpleRoundRobinProcessor(unittest.TestCase):

    def testProcess(self):
        data = np.array([1, 10, 10, 1, 10])
        p = sp.SimpleRoundRobinProcessor(3)

        for idx, prediction in np.ndenumerate(data):
            p.process(prediction, prediction)

        self.assertListEqual(p.real_node_counters, [2, 20, 10])
        self.assertListEqual(p.predict_node_counters, [2, 20, 10])
