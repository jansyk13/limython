import logging as log
import numpy as np
import pandas as pd
from itertools import chain


def parse(dataframe, limit=None):
    log.info("action=url_parse status=start")
    values = _remove_query_params(dataframe['url'].values.tolist())
    values = list(chain.from_iterable([_split(val, limit) for val in values]))
    values = _deduplicate(values)

    new_df = dataframe.copy()
    count = 0
    log.info("action=url_parse values_size=%s" % len(values))
    for value in values:
        if (count % 100 == 0):
            log.info("action=url_parse count=%s" % count)
        new_column = np.zeros(shape=(len(dataframe.index), 1))
        idx = 0
        for url in new_df['url'].values:
            if (url.startswith(value)):
                new_column[idx, 0] = 1
            idx = idx + 1
        new_df = pd.concat([new_df, pd.DataFrame(
            data=new_column, columns=['url-' + value])], axis=1)
        count = count + 1

    new_df.__delitem__('url')
    log.info("action=url_parse status=end")
    return new_df


def _split(url, limit=None):
    splits = url.split("/")
    splits = ["/".join(splits[:i + 2]) for i, split in enumerate(splits)]
    if (limit):
        splits = splits[:limit]
    return splits


def _remove_query_params(row):
    _row = row
    if "?" in _row[-1]:
        _row[-1] = _row[-1].split('?', 1)[0]
    return _row


def _deduplicate(seq):
    checked = []
    for e in seq:
        if e not in checked:
            checked.append(e)
    return checked
