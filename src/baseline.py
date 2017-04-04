#!/usr/bin/env python
import argparse
import logging as log
import MySQLdb
import pandas as pd
import pandas.io.sql as pdsql
import processors.selector as ps
import processors.utils as processor_utils
import sys
import validation.kfold_baseline as kfold

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
    parser.add_argument("-r", "--run", required=True,
                        help="'true' or 'false' whether to run full with processor")
    args = parser.parse_args()
    log.info('action=args values="%s"' % args)
    return args


def main_wrapper():
    log.info("action=main status=start")
    args = process_args()
    conn = MySQLdb.connect(host="localhost", user="root",
                           passwd="password", db="mlrl")

    dataframe = pdsql.read_sql_query(
        "SELECT payload_size FROM data LIMIT %s" % (args.limit),
        conn
    )

    if (args.run and args.run == u'true'):
        processor = ps.select_processor(args)
        predictions = dataframe['payload_size'].as_matrix()
        rmse, rsquarred = processor_utils.process_and_compute_stats(
            processor, dataframe, predictions)

        log.info("action=results counter=%s rmse=%s rsquarred=%s" %
                 (processor.node_counters, rmse, rsquarred))

    if (args.k_folds):
        validator = kfold.KfoldBaseline(ps.select_processor_supplier(
            args), dataframe, args.k_folds, args)
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
