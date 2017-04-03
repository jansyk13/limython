
import numpy.testing as npt
import logging as log
import pandas as pd
import sys
import unittest
import transformation.url as url

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestUtils(unittest.TestCase):

    def testParse(self):
        
