import logging as log
import json
import numpy as np
import transformation.url as url


def transform(requests):
    log.info('action=distinct-values')
    # create distinct values for labels
    distinct_sources = _distinct(requests, lambda x: x.source)
    distinct_methods = _distinct(requests, lambda x: x.method)
    distinct_protocols = _distinct(requests, lambda x: x.protocol)
    distinct_statuses = _distinct(requests, lambda x: x.status)
    log.info('action=labels status=start')
    # concating lists
    labels = []
    labels.extend(distinct_sources)
    labels.extend(distinct_methods)
    labels.extend(distinct_protocols)
    labels.extend(distinct_statuses)
    log.info('action=labels status=end values=\'%s\'', labels)
    size = len(labels)
    # number of requests, has to iterate over - using generator
    request_count = sum([1 for request in requests])
    # create matrix full of 0 and keep data type float64 for BLAS
    matrix = np.zeros(shape=(request_count, size))
    log.info('action=initialized matrix shape=(%s,%s)' % (request_count, size))
    payloads = []
    row_index = 0
    for request in requests:
        # fill matrix with data - indicator variables are 0/1
        log.info('action=filling-matrix status=start index=%s value=\'%s\''
                 % (row_index, json.dumps(request.__dict__)))
        column_index = distinct_sources.index(request.source)
        log.debug('action=setting_value type=source index=(%s,%s)' %
                  (row_index, column_index))
        matrix[row_index, column_index] = 1
        column_index = len(distinct_sources) +\
            distinct_methods.index(request.method)
        log.debug('action=setting_value type=method index=(%s,%s)' %
                  (row_index, column_index))
        matrix[row_index, column_index] = 1
        column_index = len(distinct_sources) +\
            len(distinct_methods) +\
            distinct_protocols.index(request.protocol)
        log.debug('action=setting_value type=protocol index=(%s,%s)' %
                  (row_index, column_index))
        matrix[row_index, column_index] = 1
        column_index = len(distinct_sources) +\
            len(distinct_methods) +\
            len(distinct_protocols) +\
            distinct_statuses.index(request.status)
        log.debug('action=setting_value type=status index=(%s,%s)' %
                  (row_index, column_index))
        matrix[row_index, column_index] = 1
        payloads.append(request.payload_size)
        row_index += 1
        log.info('action=filling-matrix status=end')

    url_parser = url.MatrixUrlParser()
    url_matrix, url_labels = url_parser.parse([row.url for row in requests])

    log.info('action=concate status=start')
    matrix_with_url = np.concatenate((matrix, url_matrix), 1)
    labels.extend(url_labels)
    log.info('action=concate status=end')

    return matrix_with_url, payloads, labels


def _distinct(seq, function):
    checked = []
    for e in seq:
        v = function(e)
        if v not in checked:
            checked.append(v)
    return checked
