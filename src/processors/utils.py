import numpy as np
import pandas as pd


def process_and_compute_stats(processor, dataframe, predictions):
    average_payload_size = dataframe['payload_size'].mean()
    _length = len(dataframe.index)
    real = dataframe['payload_size'].as_matrix()

    rmse = np.array((predictions - real) ** (2)).sum()
    rsquarred_upper = np.array((real - predictions) ** (2)).sum()
    rsquarred_lower = np.array((real - average_payload_size) ** (2)).sum()

    for idx, prediction in extract(predictions):
        processor.process(prediction)

    rmse = (rmse / _length) ** (1 / 2)
    rsquarred = 1 - (rsquarred_upper/rsquarred_lower)
    return float(rmse), float(rsquarred)

def extract(predictions):
    if (type(predictions).__module__ == np.__name__):
        return np.ndenumerate(predictions)
    return predictions
