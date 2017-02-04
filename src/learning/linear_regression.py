import transformation.data as data
from models.request import Request
import transformation.url as url
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
        self.ws = self._least_squared_regression_with_generalized_inverse(
            matrix, payloads)

    def test(self, requests, adjust_function=None):
        log.info('action=test status=start')
        sum_actual = 0
        descriptors_matrix = np.empty((0, len(self.labels)))
        to_add = []

        # create and concatenate descriptors
        for request in requests:
            descriptor_matrix = np.array([self._desribe(request)])
            to_add.append(descriptor_matrix)
            sum_actual = sum_actual + request.payload_size
        descriptors_matrix = np.concatenate(
            (descriptors_matrix, *to_add), 0)
        predicted = np.dot(descriptors_matrix, self.ws)

        # adjust prediction and collect
        _adjusted_predictions = []
        for idx, prediction in enumerate(predicted[0:]):
            _prediction = prediction
            if adjust_function is not None:
                _prediction = adjust_function(_prediction)
            _adjusted_predictions.append(_prediction)

        # count deviations + set predicted value to request
        deviations = []
        _requests = []
        for idx, request in enumerate(requests):
            dev = request.payload_size - _adjusted_predictions[idx]
            deviations.append(dev)
            _req = Request.clone_with_predicted(
                request, int(_adjusted_predictions[idx]))
            _requests.append(_req)

        # sum absolute values of deviations
        sum_dev = 0
        for dev in deviations:
            sum_dev = sum_dev + abs(dev)

        # average deviation in percentage
        avg_deviation = (100 / sum_actual) * sum_dev
        log.info('action=prediction deviation=%s' % avg_deviation)
        log.info('action=test status=end')
        return deviations, avg_deviation, _requests

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

    def _transform(self, requests):
        return data.transform(requests)

    def _least_squared_regression(self, x_array, y_array):
        log.info('action=least-squared-regression status=start size=\'%s,%s\'' %
                 (x_array.shape[0], x_array.shape[1]))
        x_mat = np.mat(x_array)
        y_mat = np.mat(y_array).T
        xt_x = x_mat.T * x_mat
        if np.linalg.det(xt_x) == 0.0:
            raise Exception("Singular matrix")
        ws = xt_x.I * (x_mat.T * y_mat)
        log.info('action=least-squared-regression status=end')
        return ws

    def _least_squared_regression_with_generalized_inverse(self, x_array, y_array):
        log.info('action=least-squared-regression-generalized-inverse status=start size=\'%s,%s\'' %
                 (x_array.shape[0], x_array.shape[1]))
        x_mat = np.mat(x_array)
        y_mat = np.mat(y_array).T
        xt_x = x_mat.T * x_mat
        ws = np.linalg.pinv(xt_x) * (x_mat.T * y_mat)
        log.info('action=least-squared-regression-generalized-inverse status=end')
        return ws
