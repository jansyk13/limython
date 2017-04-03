import logging as log
from sklearn import linear_model
import learning.utils as utils


# http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
class Ols:

    def __init__(self, kwargs):
        log.info("action=init kwargs=%s" % kwargs)
        self.args = utils._parse_kwargs(kwargs)

    def learn(self, y, x):
        log.info("action=learning status=start")
        self.model = linear_model.LinearRegression(**self.args)
        self.model.fit(x, y)
        log.info("action=learning status=end")

    def predict(self, dataframe):
        log.info("action=predict status=start")
        if (not self.model):
            raise Exception

        result = self.model.predict(dataframe)

        log.info("action=predict status=end")
        return result
