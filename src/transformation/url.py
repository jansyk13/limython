import logging as log
import numpy as np
import pandas as pd
from itertools import chain


def parse(dataframe):
    data, index, labels = _parse(dataframe)
    return pd.DataFrame(data=data, index=index, columns=labels)


def _parse(dataframe):
    log.info("action=url_parase status=start")
    values = _remove_query_params(dataframe['url'].values.tolist())
    values = list(chain.from_iterable([_split(val) for val in values]))
    values = _deduplicate(values)

    log.info("action=url_parase status=end")
    return values
    # return parse(new_matrix, values, labels)


def _split(url):
    splits = url.split("/")
    return ["/".join(splits[:i + 2]) for i, split in enumerate(splits)]


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
