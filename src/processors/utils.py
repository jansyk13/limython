import numpy as np
import pandas as pd


def process_and_compute_stats(processor, dataframe, predictions):
    average_payload_size = dataframe['payload_size'].mean()
    rmse = 0
    rsquarred_upper = 0
    rsquarred_lower = 0
    _length = len(dataframe.index)
    for idx, prediction in extract(predictions):
        processor.process(prediction)
        real_value = dataframe.iloc[idx]['payload_size'].item()
        real_prediction = prediction.item()
        rmse = rmse + \
            (real_value - real_prediction) ** (2)
        rsquarred_upper = rsquarred_upper + \
            (real_value - real_prediction) ** (2)
        rsquarred_lower = rsquarred_lower + \
            (real_value - average_payload_size) ** (2)

    rmse = (1 / ((_length) ** (1 / 2))) * (rmse ** (1 / 2))
    rsquarred = 1 - (rsquarred_upper / rsquarred_lower)
    return float(rmse), float(rsquarred)


def extract(predictions):
    if (type(predictions) is pd.Series):
        return predictions.iteritems()
    if (type(predictions).__module__ == np.__name__):
        return np.ndenumerate(predictions)
    return predictions
