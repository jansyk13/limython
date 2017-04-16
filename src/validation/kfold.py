import logging as log
import numpy as np
from sklearn.model_selection import GroupKFold
import processors.utils as processor_utils
import processors.dummy_processor as processor
import validation.utils as utils


class Kfold:

    def __init__(self, model_supplier, processor_supplier, dataframe, headers, kfolds, args):
        log.info("action=init")
        self.model_supplier = model_supplier
        self.processor_supplier = processor_supplier
        self.dataframe = dataframe
        self.headers = headers
        self.kfolds = kfolds
        self.args = args

    def validate(self):
        log.info("action=validate status=start kfolds=%s" % self.kfolds)
        group_kfold = GroupKFold(n_splits=self.kfolds)
        groups = utils.groups(self.kfolds, len(self.dataframe.index))
        idx = 0
        for train_index, test_index in group_kfold.split(self.dataframe[self.headers], self.dataframe['payload_size'], groups):
            idx = idx + 1
            dataframe_train = self.dataframe.iloc[train_index]
            dataframe_test = self.dataframe.iloc[test_index]
            model = self.model_supplier(self.args)
            model.learn(y=dataframe_train['payload_size'],
                        x=dataframe_train[self.headers])
            predictions = model.predict(dataframe_test[self.headers])
            processor = self.processor_supplier(self.args)
            rmse, rsquarred = processor_utils.process_and_compute_stats(
                processor, dataframe_test, predictions)

            log.info("action=kfold index=%s counter=%s rmse=%s rsquarred=%s" %
                     (idx, processor.real_node_counters, rmse, rsquarred))

        log.info("action=validate status=end")
