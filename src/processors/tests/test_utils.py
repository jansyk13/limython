import logging as log
import numpy as np
import pandas as pd
import sys
import unittest
import processors.utils as utils
import processors.dummy_processor as d
import processors.simple_processor as s

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestUtils(unittest.TestCase):

    def testProcess(self):
        df = pd.DataFrame({"payload_size": [10, 20, 30, 40, 50]})
        p = np.array([10, 20, 30, 40, 50])
        rmse, rsquarred = utils.process_and_compute_stats(
            d.DummyProcessor(), df, p)

        self.assertEqual(rmse, 0)
        self.assertEqual(rsquarred, 1.0)

    def testCountUtilization(self):
        processor = s.SimpleRoundRobinProcessor(3)
        processor.process(1,1)
        processor.process(2,2)
        utilization = utils.count_utilization(processor)

        self.assertEqual(utilization, [1.0, 2.0, 0.0])

    def testCountUtilizationZeroes(self):
        processor = s.SimpleRoundRobinProcessor(3)
        processor.process(0,0)
        processor.process(0,0)
        utilization = utils.count_utilization(processor)

        self.assertEqual(utilization, [0.0, 0.0, 0.0])

    def testCountUtilizationDummy(self):
        utilization = utils.count_utilization(d.DummyProcessor())

        self.assertEqual(utilization, [])
