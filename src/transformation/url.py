import logging as log
import numpy as np

# Transforms url into tree based binary values
# Example:
# A/B/C
# A/B/D
# To:
# A B C D
# 1 1 1 0
# 1 1 0 1


class MatrixUrlParser:

    def __init__(self):
        log.info('action=init')

    def parse(self, list):
        values = [remove_query_params(value.split("/")) for value in list]
        length = len(values)
        matrix = np.empty((length, 0))
        return self._parse(matrix, values, [])

    def _parse(self, matrix, values, labels):
        log.info("action=_parse matrix=%s labels=(%s)" % (matrix.shape, len(labels)))
        _first_values = []
        for value in values:
            if len(value) > 0:
                _first_values.append(value[0])
        if len(_first_values) == 0:
            return matrix, labels
        _distinct_first_values = deduplicate(_first_values)
        labels.extend(_distinct_first_values)

        new_columns = np.zeros((len(values), len(_distinct_first_values)))
        _idx = 0
        for row in values:
            if (len(row) > 0):
                _decide_on = row.pop(0)
                _index = _distinct_first_values.index(_decide_on)
                log.info('action=setting_value_in_new_columns indexes=(%s,%s)' %
                         (_idx, _index))
                new_columns[_idx, _index] = 1
            _idx = _idx + 1
        log.info('action=concatenate status=start')
        new_matrix = np.concatenate((matrix, new_columns), 1)
        log.info('action=concatenate status=end')
        return self._parse(new_matrix, values, labels)


def remove_query_params(row):
    _row = row
    if "?" in _row[-1]:
        _row[-1] = _row[-1].split('?', 1)[0]
    return _row


def deduplicate(seq):
    checked = []
    for e in seq:
        if e not in checked:
            checked.append(e)
    return checked
