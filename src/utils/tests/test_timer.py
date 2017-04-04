import logging as log
import utils.timer as timer
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestTimer(unittest.TestCase):

    def testTimer(self):
        t = timer.start()
        timer.stop(t)

        self.assertIsNotNone(t)
