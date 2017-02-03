import transformation.data as data
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
        raise Exception(
            'Not implemented due matrix being singulard all the time...')

    def test(self, requests):
        raise Exception(
            'Not implemented due matrix being singulard all the time...')

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
