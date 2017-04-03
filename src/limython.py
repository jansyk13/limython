#!/usr/bin/env python
import argparse
import MySQLdb
import logging as log
import learning.ols as ols
import learning.lasso as lasso
import learning.sgd as sgd
import learning.ridge as ridge
import learning.tree as tree
import numpy as np
import pandas as pd
import pandas.io.sql as pdsql
import processors.simple_processor
import processors.best_counter_processor
import processors.utils as processor_utils
import sys
import transformation.categorical as categorical
import validation.kfold as kfold
import blas as blas

log.basicConfig(stream=sys.stdout, level=log.INFO,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


def regression_tree_supplier(args):
    return tree.Tree(args.arguments)


def ols_regression_supplier(args):
    return ols.Ols(args.arguments)


def ridge_regression_supplier(args):
    return ridge.Ridge(args.arguments)


def sgd_regression_supplier(args):
    return sgd.Sgd(args.arguments)


def lasso_regression_supplier(args):
    return lasso.Lasso(args.arguments)


def select_model_supplier(args):
    case = {
        'ols': ols_regression_supplier,
        'lasso': lasso_regression_supplier,
        'ridge': ridge_regression_supplier,
        'sgd': sgd_regression_supplier,
        'tree': regression_tree_supplier
    }
    select_function = case[args.model]
    log.info('action=selecting-model value=%s' % args.model)
    return select_function


def select_model(args):
    select_function = select_model_supplier(args)
    return select_function(args)


def best_counter_processor_supplier(args):
    return processors.best_counter_processor.BestCounterProcessor(args.node_count)


def simple_round_robin_supplier(args):
    return processors.simple_processor.SimpleRoundRobinProcessor(args.node_count)


def select_processor(args):
    case = {
        'simple-round-robin': simple_round_robin_supplier,
        'best-counter': best_counter_processor_supplier,
    }
    select_function = case[args.processor]
    log.info('action=selecting-processor value=%s' % args.processor)
    return select_function(args)


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
    processor = select_processor(args)
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

    model = select_model(args)
    model.learn(y=dataframe['payload_size'],
                x=dataframe[headers])
    predictions = model.predict(dataframe[headers])

    rmse, rsquarred = processor_utils.process_and_compute_stats(
        processor, dataframe, predictions)

    log.info("action=results counter=%s rmse=%s rsquarred=%s" %
             (processor.node_counters, rmse, rsquarred))

    if (args.k_folds):
        validator = kfold.Kfold(select_model_supplier(
            args), dataframe, headers, args.k_folds, args)
        validator.validate()
    log.info("action=main status=end")


def main():
    try:
        with blas.utils.num_threads(32):
            main_wrapper()
    except Exception:
        log.info('action=end-with-exception')
        raise

if __name__ == "__main__":
    main()
