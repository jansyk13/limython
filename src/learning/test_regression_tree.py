import learning.regression_tree as tree
import logging as log
import numpy as np
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class LinearRegressionTest(unittest.TestCase):

    def testBinSplit(self):
        matrix = np.array([[1, 10, 1], [1, 5, 1], [1, 10, 1]])

        left, right = tree._bin_split_matrix(matrix, 1, 7)

        self.assertTrue(np.array_equal(left, [[1, 10, 1], [1, 10, 1]]))
        self.assertTrue(np.array_equal(right, [[1, 5, 1]]))

    def testRegLeaf(self):
        matrix = np.array([[1, 5], [1, 10], [1, 15]])

        mean = tree._reg_leaf(matrix)

        self.assertEqual(mean, 10)

    def testRegError(self):
        matrix = np.array([[1, 5], [1, 10], [1, 15]])

        variance = tree._reg_error(matrix)

        self.assertEqual(variance, 50)

    def testNoMoreSplits(self):
        self.assertFalse(tree._no_more_splits(
            np.array([[0, 0, 1], [0, 0, 2]])))
        self.assertTrue(tree._no_more_splits(np.array([[0, 0, 1], [0, 0, 1]])))

    def testChooseSplit(self):
        matrix = np.array([[2, 0, 5], [1, 0, 10], [2, 1, 5]])

        learning = tree.RegressionTree()

        feature, value, to_skip = learning._choose_split(
            matrix, tree._reg_leaf, tree._reg_error, 1, 1, [], 1)

        self.assertEqual(feature, 0)
        self.assertEqual(value, 1)

    def testCreateTree(self):
        matrix = np.array([[2, 0, 5], [1, 0, 10], [2, 1, 5], [0, 1, 15]])

        learning = tree.RegressionTree()

        _tree = learning._create_tree(
            matrix, tree._reg_leaf, tree._reg_error, 1, 1)

        self.maxDiff = None
        self.assertEqual(_tree.to_json(), '{"feature": 0, "left_child": {"feature": '
                         'null, "left_child": null, "right_child": null, "value": 5.0}, '
                         '"right_child": {"feature": 0, "left_child": {"feature": null, '
                         '"left_child": null, "right_child": null, "value": 10.0}, '
                         '"right_child": {"feature": null, "left_child": null, '
                         '"right_child": null, "value": 15.0}, "value": "0"}, '
                         '"value": "1"}')

    def testJoinMatrixWithPayloads(self):
        matrix = np.array([[1, 0, 1], [1, 0, 1], [0, 1, 1], [0, 1, 1]])
        payloads = np.array([[10, 10, 10, 10]]).T

        final = np.concatenate((matrix, payloads), 1)

        self.assertTrue(np.array_equal(
            final, [[1, 0, 1, 10], [1, 0, 1, 10], [0, 1, 1, 10], [0, 1, 1, 10]]), 'Not equal final=%s' % final)
