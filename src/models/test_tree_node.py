from models.tree_node import Node
import learning.regression_tree as tree
import numpy as np
import logging as log
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class TreeNodeTest(unittest.TestCase):

    def testApply(self):
        matrix = np.array([[2, 0, 5], [1, 0, 10], [2, 1, 5], [0, 1, 15]])

        learning = tree.RegressionTree()

        _tree = learning._create_tree(
            matrix, tree._reg_leaf, tree._reg_error, 1, 1)

        result = _tree.apply(np.array([2, 1]))

        self.assertEqual(result, 5)
