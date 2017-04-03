import logging as log
import learning.utils as utils
from sklearn import tree
import re

# http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html#sklearn.tree.DecisionTreeRegressor


class Tree:

    def __init__(self, kwargs):
        log.info("action=init kwargs=%s" % kwargs)
        self.args = utils._parse_kwargs(kwargs)

    def learn(self, y, x):
        log.info("action=learning status=start")
        self.model = tree.DecisionTreeRegressor(**self.args)
        self.model.fit(x, y)
        log.info("action=learning status=end")

    def predict(self, dataframe):
        log.info("action=predict status=start")
        if (not self.model):
            raise Exception

        result = self.model.predict(dataframe)

        log.info("action=predict status=end")
        return result
