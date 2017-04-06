#!/usr/bin/env python
import argparse
import learning.selector as ls
import logging as log
import MySQLdb
import numpy as np
import pandas as pd
import pandas.io.sql as pdsql
import processors.selector as ps
import processors.utils as processor_utils
import sys
import transformation.categorical as categorical
import validation.kfold as kfold

log.basicConfig(stream=sys.stdout, level=log.INFO,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--processor", required=True,
                        help="Request processor(simple-round-robin,best-counter)")
    parser.add_argument("-n", "--node-count", required=True,
                        help="Node count for processor(1,2,3,...)")
    parser.add_argument("-l", "--limit", required=True,
                        help="Data limit(to avoid running out of memory)")
    parser.add_argument("-k", "--k-folds", type=int, default=2,
                        help="Number of folds for cross validation(higher better, but computation more expensive)")
    parser.add_argument("-m", "--model", required=True,
                        help="ML model(ols, lasso, ridge, sgd, tree)")
    parser.add_argument("-a", "--arguments",
                        help="ML model arguments - kwargs separated with comma")
    parser.add_argument("-u", "--url", default='false',
                        help="Flag whether url should be parsed into tree like indicators")
    parser.add_argument("-ul", "--url-limit", type=int, default=None,
                        help="Limit depth of tree hierarchy of dummy variable parsed from urls")
    parser.add_argument("-f", "--features", type=str, default='*',
                        help="List of features - comma separated")
    parser.add_argument("-r", "--run", required=True,
                        help="'true' or 'false' whether to run full with processor")
    args = parser.parse_args()
    log.info('action=args values="%s"' % args)
    return args


def to_omit(url):
    omit = ["payload_size"]
    if (url and url == u'true'):
        # omit url because it will parsed separate way
        omit.append('url')
    return omit


def main_wrapper():
    log.info("action=main status=start")
    args = process_args()
    conn = MySQLdb.connect(host="localhost", user="root",
                           passwd="password", db="mlrl")
    _to_omit = to_omit(args.url)

    dataframe, headers = categorical.tranform(
        pdsql.read_sql_query(
            "SELECT %s FROM data LIMIT %s" % (args.features, args.limit),
            conn
        ),
        _to_omit,
        args.url,
        args.url_limit
    )

    if (args.run and args.run == u'true'):
        processor = ps.select_processor(args)
        model = ls.select_model(args)
        model.learn(y=dataframe['payload_size'],
                    x=dataframe[headers])
        predictions = model.predict(dataframe[headers])

        rmse, rsquarred = processor_utils.process_and_compute_stats(
            processor, dataframe, predictions)

        log.info("action=results counter=%s rmse=%s rsquarred=%s" %
                 (processor.node_counters, rmse, rsquarred))

    if (args.k_folds and args.k_folds is not -1):
        validator = kfold.Kfold(ls.select_model_supplier(args), ps.select_processor_supplier(
            args), dataframe, headers, args.k_folds, args)
        validator.validate()
    log.info("action=main status=end")


def main():
    try:
        main_wrapper()
    except Exception:
        log.info('action=end-with-exception')
        raise

if __name__ == "__main__":
    main()
