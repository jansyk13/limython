from models.request import Request
import processors.best_counter_processor_with_predicted as processor
import logging as log
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class BestCounterProcessorWithPredictedTest(unittest.TestCase):

    def testProcess(self):
        _processor = processor.BestCounterProcessorWithPredicted(node_count=3)

        req1 = Request(1, '127.0.0.1', '30:13:57:47',
                       'GET', 'A/B/C', 'HTTP 1.1', 200, 200)
        req1.predicted_payload_size = 250
        _processor.process(req1)
        _processor.process(req1)
        _processor.process(req1)

        self.assertEqual(_processor.node_counters, [200, 200, 200])
        self.assertEqual(_processor.predicted_node_counters, [250, 250, 250])
