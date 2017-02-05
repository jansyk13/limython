from models.tree_node import Node
from models.request import Request
import concurrent.futures
import multiprocessing

import transformation.data as data
import logging as log
import numpy as np
import transformation.url as url
import time

# CART algorithm with Shannon entropy


class RegressionTree:

    def __init__(self):
        log.info('action=init')
        self.entropy_executor = concurrent.futures.ThreadPoolExecutor(
            multiprocessing.cpu_count()*20)

    def learn(self, requests):
        matrix, payloads, labels = self._transform(requests)
        self.matrix = matrix
        self.labels = labels
        self.payloads = payloads
        _matrix = np.concatenate((matrix, np.array([payloads]).T), 1)
        log.info('action=tree status=start')
        self.tree = self._create_tree(
            _matrix, _reg_leaf, _reg_error, 1, 10)
        log.debug('action=tree status=end value=%s' %
                  self.tree.to_json(indent=1))
        log.info('action=tree status=end')

    def test(self, requests, adjust_function=None):
        log.info('action=test status=start')
        descriptors_matrix = np.empty((0, len(self.labels)))
        to_add = []
        payloads = []

        # create and concatenate descriptors
        for request in requests:
            descriptor_matrix = np.array([self._desribe(request)])
            to_add.append(descriptor_matrix)
            payloads.append(request.payload_size)
        matrix = np.concatenate((descriptors_matrix, *to_add), 0)

        matrix, payloads, labels = self._transform(requests)
        sum_payloads = np.sum(payloads)
        results = []
        log.info('action=applying-result status=start')
        for idx, request_matrix in enumerate(matrix):
            if idx % 100 == 0:
                log.info('action=applying-result status=running id=%s' % idx)
            results.append(self.tree.apply(request_matrix))
        log.info('action=applying-result status=end')
        sum_predictions = np.sum(np.array(results))
        deviations = []
        _requests = []
        for idx, request in enumerate(requests):
            _prediction = results[idx]
            if adjust_function is not None:
                _prediction = adjust_function(_prediction)
            deviations.append(payloads[idx] - _prediction)
            _requests.append(Request.clone_with_predicted(
                request, _prediction))

        avg_deviation = (100 / sum_payloads) * sum_predictions
        log.info('action=prediction deviation=%s' % avg_deviation)
        log.info('action=test status=end')
        return deviations, avg_deviation, _requests

    def _transform(self, requests):
        return data.transform(requests)

    def _create_tree(self, matrix, leaf_type, error_type, max_error, min_leaf_size, to_skip=[], depth=0):
        log.info('action=_create_tree status=start depth=%s' % depth)
        feature, value, add_to_skip = self._choose_split(
            matrix, leaf_type, error_type, max_error, min_leaf_size, to_skip, (depth + 1))
        if feature is None:
            return Node.only_value(value)
        if (add_to_skip == True and len(set(matrix[:, feature])) == 2):
            to_skip.append(feature)
        left, right = _bin_split_matrix(matrix, feature, value)
        _right = self._create_tree(
            right, leaf_type, error_type, max_error, min_leaf_size, list(to_skip), (depth + 1))
        _left = self._create_tree(
            left, leaf_type, error_type, max_error, min_leaf_size, list(to_skip), (depth + 1))
        log.info('action=_create_tree status=end depth=%s' % depth)
        return Node(feature, value, _left, _right)

    def _choose_split(self, matrix, leaf_type, error_type, max_error, min_leaf_size, to_skip, depth):
        log.info('action=_choose_split status=start depth=%s' % depth)
        if _no_more_splits(matrix):
            log.info(
                'action=_choose_split status=end-no-more-splits depth=%s' % depth)
            return None, leaf_type(matrix), False
        m, n = np.shape(matrix)
        _current_entropy = error_type(matrix)
        _best_entropy = np.inf
        _best_index = 0
        _best_value = 0
        # zero based indexing + last index is omitted
        for _idx in range(n - 1):
            if _idx % 100 == 0:
                log.info('action=_choose_split id=%s' % _idx)
            if _idx in to_skip:
                continue
            _set = set(matrix[:, _idx])
            futures = []
            for _val in _set:
                _f = self.entropy_executor.submit(
                    _calculate_entropy, matrix, leaf_type,
                    error_type, _idx, _val, min_leaf_size)
                futures.append(_f)
            results = [_f.result() for _f in futures]
            best_result = min(results, key=lambda item: item[0])
            if best_result[0] < _best_entropy:
                _best_index = best_result[1]
                _best_value = best_result[2]
                _best_entropy = best_result[0]
        if (_current_entropy - _best_entropy) < max_error:
            log.info(
                'action=_choose_split status=end-not-enough-information-gain depth=%s' % depth)
            return None, leaf_type(matrix), False
        _left, _right = _bin_split_matrix(matrix, _best_index, _best_value)
        if (np.shape(_left)[0] < min_leaf_size) or (np.shape(_right)[0] < min_leaf_size):
            log.info('action=_choose_split status=end-leaf-size depth=%s' % depth)
            return None, leaf_type(matrix), False
        log.info('action=_choose_split status=end depth=%s' % depth)
        return _best_index, _best_value, True

    def _desribe(self, request):
        descriptor_matrix = np.zeros(len(self.labels))
        if request.source in self.labels:
            descriptor_matrix[self.labels.index(request.source)] = 1
        if request.method in self.labels:
            descriptor_matrix[self.labels.index(request.method)] = 1
        if request.protocol in self.labels:
            descriptor_matrix[self.labels.index(request.protocol)] = 1
        if request.status in self.labels:
            descriptor_matrix[self.labels.index(request.status)] = 1
        for _url in url.remove_query_params(url.split(request.url)):
            if _url in self.labels:
                descriptor_matrix[self.labels.index(_url)] = 1
        return descriptor_matrix


def _calculate_entropy(matrix, leaf_type, error_type, _idx, _val, min_leaf_size):
    _left, _right = _bin_split_matrix(matrix, _idx, _val)
    if (np.shape(_left)[0] < min_leaf_size) or (np.shape(_right)[0] < min_leaf_size):
        return np.inf, 0, 0
    return error_type(_left) + error_type(_right), _idx, _val


def _reg_leaf(matrix):
    # using mean value
    log.debug('action=_reg_leaf')
    return np.mean(matrix[:, -1])


def _reg_error(matrix):
    # using variance of values
    log.debug('action=_reg_error')
    return np.var(matrix[:, -1]) * np.shape(matrix)[0]


def _bin_split_matrix(matrix, feature, value):
    _left_matrix = matrix[np.nonzero(matrix[:, feature] > value)[0], :]
    if (_left_matrix.shape[0] == 0):
        # short circuting
        return _left_matrix, matrix
    _right_matrix = matrix[np.nonzero(matrix[:, feature] <= value)[0], :]
    return _left_matrix, _right_matrix


def _no_more_splits(matrix):
    return len(set(matrix[:, -1].T.tolist())) == 1
