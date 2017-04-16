import logging as log
import numpy as np
from sklearn.model_selection import GroupKFold
import processors.utils as processor_utils
import processors.dummy_processor as processor
import validation.utils as utils


class KfoldBaseline:

    def __init__(self, processor_supplier, dataframe, kfolds, args):
        log.info("action=init")
        self.processor_supplier = processor_supplier
        self.dataframe = dataframe
        self.kfolds = kfolds
        self.args = args

    def validate(self):
        log.info("action=validate-baseline status=start kfolds=%s" %
                 self.kfolds)
        group_kfold = GroupKFold(n_splits=self.kfolds)
        groups = utils.groups(self.kfolds, len(self.dataframe.index))
        idx = 0
        for train_index, test_index in group_kfold.split(self.dataframe['payload_size'], self.dataframe['payload_size'], groups):
            idx = idx + 1
            dataframe = self.dataframe.iloc[train_index]
            processor = self.processor_supplier(self.args)
            predictions = dataframe['payload_size'].as_matrix()
            rmse, rsquarred = processor_utils.process_and_compute_stats(
                processor, dataframe, predictions)

            log.info("action=kfold index=%s counter=%s rmse=%s rsquarred=%s" %
                     (idx, processor.real_node_counters, rmse, rsquarred))

        log.info("action=validate-baseline status=end")
