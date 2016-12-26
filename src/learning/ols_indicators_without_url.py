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
        # create distinct values for labels
        distinct_sources = self._distinct(requests, lambda x: x.source)
        distinct_methods = self._distinct(requests, lambda x: x.method)
        distinct_protocols = self._distinct(requests, lambda x: x.protocol)
        distinct_statuses = self._distinct(requests, lambda x: x.status)
        log.info('action=labels status=start')
        # concating lists
        labels = []
        labels.extend(distinct_sources)
        labels.extend(distinct_methods)
        labels.extend(distinct_protocols)
        labels.extend(distinct_statuses)
        labels.append('payload_size')
        log.info('action=labels status=end values=\'%s\'', labels)
        size = len(labels)
        # number of requests, has to iterate over - using generator
        request_count = sum([1 for  request in requests])
        # create matrix and set type uint16 to keep memory consuption low
        matrix = np.zeros(shape=(size, request_count))
        index = 0
        for request in requests:
            # fill matrix with data - indicator variables are 0/1
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
        log.info('action=standard-regression status=start size=\'%s,%s\'' % (x_array.shape[0], x_array.shape[1]))
        x_mat = np.mat(x_array)
        gc.collect()
        log.info('action=gc-called after=\'np.mat(x_array)\'')
        y_mat = np.mat(y_array).T
        gc.collect()
        log.info('action=gc-called after=\'np.mat(y_array).T\'')
        xt = x_mat.T
        gc.collect()
        log.info('action=gc-called after=\'x_mat.T\'')
        xt_x =  np.dot(xt, x_mat)
        gc.collect()
        log.info('action=gc-called after=\'xt * x_mat\'')
        if np.linalg.det(xt_x) == 0.0:
            log.info("action=matrix-singular-cannot-inverse status=error")
            raise Exception('Matrix is singular')
        gc.collect()
        log.info('action=gc-called after=\'det(xt_x)\'')
        xt_x_I = xt_x.I
        gc.collect()
        log.info('action=gc-called after=\'xt_x_I\'')
        ws = np.dot(xt_x_I,np.dot(x_mat.T,y_mat))
        gc.collect()
        log.info('action=gc-called after=\'xt_x_I * (x_mat.T * y_mat)\'')
        log.info('action=standard-regression status=end')
        return ws
