#!/usr/bin/env python

import argparse
import concurrent.futures
import data.generator as generator
import data.mysql as db
import logging as log
import processors.simple_processor
import processors.best_counter_processor
import processors.best_counter_processor_with_predicted
import sys
import time

import learning.linear_regression as regression
import learning.regression_tree as tree

import numpy as np
np.set_printoptions(threshold=np.nan)

log.basicConfig(stream=sys.stdout, level=log.INFO,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')

def adjust_function(_prediction):
    if _prediction < 0:
        return 0
    return _prediction


def select_data(data):
    case = {
        'test': 'test_data',
        'training': 'training_data'
    }
    return case[data]


def best_counter_processor_supplier(args):
    return processors.best_counter_processor.BestCounterProcessor(args.node_count)


def best_counter_with_predicted_processor_supplier(args):
    return processors.best_counter_processor_with_predicted.BestCounterProcessorWithPredicted(args.node_count)


def simple_round_robin_supplier(args):
    return processors.simple_processor.SimpleRoundRobinProcessor(args.node_count)


def select_processor(args):
    case = {
        'simple-round-robin': simple_round_robin_supplier,
        'best-counter': best_counter_processor_supplier,
        'best-counter-with-predicted': best_counter_with_predicted_processor_supplier
    }
    select_function = case[args.processor]
    log.info('action=selecting-processor value=%s' % args.processor)
    return select_function(args)


def learning(args):
    data = generator.Generator(cursor=db.get_cursor(
    ), table=select_data('training'), limit=int(args.training_limit), offset=1000)
    test_data = generator.Generator(cursor=db.get_cursor(
    ), table=select_data('test'), limit=int(args.testing_limit), offset=1000)
    if args.prediction == 'regression':
        learning = regression.LinearRegression()
        learning.learn(data)
        deviations, avg_deviation, _requests = learning.test(
            test_data, lambda x: adjust_function(x))
        return _requests
    elif args.prediction == 'tree':
        learning = tree.RegressionTree()
        learning.learn(data)
        deviations, avg_deviation, _requests = learning.test(
            test_data, lambda x: adjust_function(x))
        return _requests
    else:
        return test_data


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--processor", help="Request processor(simple-round-robin,best-counter,best-counter-with-predicted)")
    parser.add_argument("-n", "--node-count",
                        help="Node count for processor(1,2,3,...)")
    parser.add_argument("-t", "--threads",
                        help="Thread count for processor(1,2,3,...)")
    parser.add_argument(
        "-trl", "--training-limit", help="Data limit in training generators(1,2,3,...)")
    parser.add_argument(
        "-tel", "--testing-limit", help="Data limit in testing generators(1,2,3,...)")
    parser.add_argument("-pr", "--prediction",
                        help="Prediction ML model(regression,tree)")
    args = parser.parse_args()
    log.info('action=args values="%s"' % args)
    return args


def main_wrapper():
    args = process_args()
    processor = select_processor(args)
    data = learning(args)
    log.info('action=processing status=start')
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(args.threads)) as executor:
        start_time = time.time()
        executor.map(processor.process, data)
    counters_sum = sum(processor.node_counters)
    utilization = [c * int(args.node_count) /
                   counters_sum for c in processor.node_counters]
    log.info('action=processing status=end time=%s' %
             (time.time() - start_time))
    log.info('action=counters data=\'%s\' utilization=\'%s\' sum=%d' %
             (processor.node_counters, utilization, counters_sum))


def main():
    try:
        main_wrapper()
    except Exception:
        log.info('action=end-with-exception')
        raise

if __name__ == "__main__":
    main()
