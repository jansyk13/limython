import json
import logging as log
import numpy as np

class LinearRegression:
    def __init__(self):
        log.info("action=init")

    def learn(self, requests):
        matrix, payloads, labels = self._transform(requests)
        self.matrix = matrix
        self.labels = labels
        self.payloads = payloads
        self.ws = self._least_squared_regression(matrix, payloads)

    def predict(self, requests):
        raise Exception('Not implemented due matrix being singulard all the time...')

    def test(self, requests):
        raise Exception('Not implemented due matrix being singulard all the time...')

    def _transform(self, requests):
        log.info('action=distinct-values')
        # create distinct values for labels
        distinct_sources = self._distinct(requests, lambda x: x.source)
        distinct_methods = self._distinct(requests, lambda x: x.method)
        distinct_protocols = self._distinct(requests, lambda x: x.protocol)
        distinct_statuses = self._distinct(requests, lambda x: x.status)
        distinct_urls = self._distinct(requests, lambda x: x.url)
        log.info('action=labels status=start')
        # concating lists
        labels = []
        labels.extend(distinct_sources)
        labels.extend(distinct_methods)
        labels.extend(distinct_protocols)
        labels.extend(distinct_statuses)
        labels.extend(distinct_urls)
        log.info('action=labels status=end values=\'%s\'', labels)
        size = len(labels)
        # number of requests, has to iterate over - using generator
        request_count = sum([1 for  request in requests])
        # create matrix full of 0 and keep data type float64 for BLAS
        matrix = np.zeros(shape=(size, request_count))
        payloads = []
        row_index = 0
        for request in requests:
            # fill matrix with data - indicator variables are 0/1
            log.info('action=filling-matrix status=start index=%s value=\'%s\''\
                % (index, json.dumps(request.__dict__)))
            column_index = distinct_sources.index(request.source) - 1
            matrix[column_index, row_index] = 1
            column_index = len(distinct_sources) +\
                distinct_methods.index(request.method) - 1
            matrix[column_index, row_index] = 1
            column_index = len(distinct_sources) +\
                len(distinct_methods) +\
                distinct_protocols.index(request.protocol) - 1
            matrix[column_index, row_index] = 1
            column_index = len(distinct_sources) +\
                len(distinct_methods) +\
                len(distinct_protocols) +\
                distinct_statuses.index(request.status) - 1
            matrix[column_index, row_index] = 1
            column_index = len(distinct_sources) +\
                len(distinct_methods) +\
                len(distinct_protocols) +\
                len(distinct_statuses) +\
                distinct_urls(request.urls) - 1
            matrix[column_index, row_index] = 1
            payloads.append(request.payload_size)
            row_index += 1
            log.info('action=filling-matrix status=end')
        return matrix, payloads, labels

    def _distinct(self, requests, function):
        return list(set([function(request) for request in requests]))

    def _least_squared_regression(self, x_array, y_array):
        log.info('action=least-squared-regression status=start size=\'%s,%s\'' % (x_array.shape[0], x_array.shape[1]))
        x_mat = np.mat(x_array)
        y_mat = np.mat(y_array).T
        xt_x = x_mat.T * x_mat
        if np.linalg.det(xt_x) == 0.0:
            raise Exception("Singular matrix")
        ws = xt_x.I * (x_mat.T * y_mat)
        log.info('action=least-squared-regression status=end')
        return ws
