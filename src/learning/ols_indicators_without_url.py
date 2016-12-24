import gc
import json
import logging as log
import numpy as np

class LinearRegressionWithoutUrl:
    def __init__(self):
        log.info("action=init")

    def learn(self, requests):
        matrix, labels = self._transform(requests)
        self.matrix = matrix
        self.labels = labels
        self.ws = self._stand_regression(matrix, labels)

    # def predict(self, requests):


    def _transform(self, requests):
        log.info('action=distinct-values')
        distinct_sources = self._distinct(requests, lambda x: x.source)
        distinct_methods = self._distinct(requests, lambda x: x.method)
        distinct_protocols = self._distinct(requests, lambda x: x.protocol)
        distinct_statuses = self._distinct(requests, lambda x: x.status)
        log.info('action=labels status=start')
        labels = []
        labels.extend(distinct_sources)
        labels.extend(distinct_methods)
        labels.extend(distinct_protocols)
        labels.extend(distinct_statuses)
        labels.append('payload_size')
        log.info('action=labels status=end values=\'%s\'', labels)
        size = len(labels)
        request_count = sum([1 for  request in requests])
        matrix = np.zeros(shape=(size, request_count))
        index = 0
        for request in requests:
            log.info('action=filling-matrix status=start index=%s value=\'%s\'' % (index, json.dumps(request.__dict__)))
            secondary_index = distinct_sources.index(request.source) - 1
            matrix[secondary_index, index] = 1
            secondary_index = len(distinct_sources) + distinct_methods.index(request.method) - 1
            matrix[secondary_index, index] = 1
            secondary_index = len(distinct_sources) + len(distinct_methods) + distinct_protocols.index(request.protocol) - 1
            matrix[secondary_index, index] = 1
            secondary_index = len(distinct_sources) + len(distinct_methods) + len(distinct_protocols) + distinct_statuses.index(request.status) - 1
            matrix[secondary_index, index] = 1
            matrix[size-1, index] = request.payload_size
            index += 1
            log.info('action=filling-matrix status=end')
        return matrix, labels

    def _distinct(self, requests, function):
        return list(set([function(request) for request in requests]))

    def _stand_regression(self, x_array, y_array):
        x_mat = np.mat(x_array)
        y_mat = np.mat(y_array).T
        x_tx = x_mat.T * x_mat
        if np.linalg.det(x_tx) == 0.0:
            log.info("action=matrix-singular-cannot-inverse status=error")
            raise Exception('Matrix is singular')
        ws = x_tx.I * (x_mat.T * y_mat)
        return ws
