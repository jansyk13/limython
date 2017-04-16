#!/usr/bin/env python
import sys
import re
from os import listdir
from os.path import isfile, join

to_extract = sys.argv[1]
path = sys.argv[2]
files = [f for f in listdir(path) if isfile(join(path, f))]
for _file in files:
    with open(path + _file, "r") as f:
        result = []
        name = _file.replace("ols_", "").replace("ridge_", "").replace(
            "tree_", "").replace("lasso_", "").replace("sgd_", "")
        result.append(name)
        for line in f:
            if (to_extract == u'stdev'):
                if ("MainThread utils.py INFO action=utilization value=" in line):
                    r = re.search("^.*MainThread.*\[(.*)\].*$", line)
                    result.append("=STDEV(%s)" % r.group(1))
                    continue
            if (to_extract == u'rsquarred'):
                if ("MainThread kfold.py INFO action=kfold" in line):
                    r = re.search(
                        "^.*MainThread.*rmse=(.*) rsquarred=(.*).*$", line)
                    result.append("%s" % r.group(2))
                    continue
            if (to_extract == u'timer'):
                if ("MainThread timer.py INFO action=timer" in line):
                    r = re.search(
                        "^.*MainThread.*value=(.*).*$", line)
                    result.append("%s" % r.group(1))
                    continue
            if (to_extract == u'rmse'):
                if ("MainThread kfold.py INFO action=kfold" in line):
                    r = re.search(
                        "^.*MainThread.*rmse=(.*) rsquarred=(.*).*$", line)
                    result.append("%s" % r.group(1))
                    continue
            if (to_extract == u'counter'):
                if ("action=results node_count=" in line):
                    r = re.search("^.*MainThread.*\[(.*)\].*$", line)
                    result.append("%s" % r.group(1))
                    continue
        print(";".join(result))
