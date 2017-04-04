import logging as log
import numpy as np
import pandas as pd
from functools import reduce
import utils.timer as timer


def process_and_compute_stats(processor, dataframe, predictions):
    average_payload_size = dataframe['payload_size'].mean()
    _length = len(dataframe.index)
    real = dataframe['payload_size'].as_matrix()

    rmse = np.array((predictions - real) ** (2)).sum()
    rsquarred_upper = np.array((real - predictions) ** (2)).sum()
    rsquarred_lower = np.array((real - average_payload_size) ** (2)).sum()

    t = timer.start()
    for idx, prediction in np.ndenumerate(predictions):
        processor.process(prediction)
    timer.stop(t)
    utilization = count_utilization(processor)
    log.info("action=utilization value=%s" % utilization)

    rmse = (rmse / _length) ** (1 / 2)
    rsquarred = 1 - (rsquarred_upper / rsquarred_lower)
    return float(rmse), float(rsquarred)


def count_utilization(processor):
    if (len(processor.node_counters) > 0):
        n = len(processor.node_counters)
        total = reduce(lambda x, y: (x + y), processor.node_counters)
        utilization = []
        for node_counter in processor.node_counters:
            utilization.append(((100 * n / total) * node_counter) / 100)
        return utilization
    else:
        return []
