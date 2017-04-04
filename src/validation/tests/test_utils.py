import logging as log
import numpy as np
import numpy.testing as npt
import sys
import unittest
import validation.utils as utils
import learning.ols as ols
import processors.dummy_processor as dummy

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TestUtils(unittest.TestCase):

    def testGroups(self):
        groups = utils.groups(5, 11)

        npt.assert_allclose(groups, np.array(
            [0., 0., 1., 1., 2., 2., 3., 3., 4., 4., 0.]))
