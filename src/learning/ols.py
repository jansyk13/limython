import logging as log
from pandas.stats.api import ols


class Ols:

    def __init__(self):
        log.info("action=init")

    def learn(self, y, x):
        log.info("action=learning status=start")
        self.model = ols(y=y,  x=x)
        log.info("action=learning status=end")

    def predict(self, dataframe):
        log.info("action=predict status=start")
        if (not self.model):
            raise Exception

        result = self.model.predict(x=dataframe)

        log.info("action=predict status=end")
        return result
