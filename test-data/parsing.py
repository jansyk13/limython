#!/usr/bin/env python
import sys


def is_http_method(param):
    return param == u'POST' or param == u'GET' or param == u'HEAD' or param == u'OPTION' or param == u'DELETE' or param == u'PUT'

args = sys.argv
if (args and len(args) > 1):
    limit = int(args[1])
else:
    limit = None

with open('raw_data', 'r') as f:
    with open("data.sql", "a") as data_file:
        for i, line in enumerate(f):
            values = line.split()
            if (len(values) > 7):
                continue
            values[1] = values[1].strip("[]")
            values[2] = values[2].strip('"')
            if (not is_http_method(values[2])):
                values.insert(2, 'NULL')
            values[3] = values[3].strip('"')
            values[4] = values[4].strip('"')
            if (values[4] != u'HTTP/1.0'):
                values.insert(4, 'NULL')
            values[6] = values[6] if values[6] != u'-' else 0
            table = 'data'
            insert = "INSERT INTO %s (source, time_stamp, method, url, protocol, status, payload_size) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %s); \n" % (
                table, values[0], values[1], values[2], values[3], values[4], values[5], values[6])
            data_file.write(insert)
            if (limit and limit < i):
                break
