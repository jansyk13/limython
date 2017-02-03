#!/usr/bin/env python

import argparse
import concurrent.futures
import data.generator as generator
import data.mysql as db
import logging as log
import processors.simple_processor
import processors.best_counter_processor
import sys
import time

import learning.linear_regression as regression

import numpy as np
np.set_printoptions(threshold=np.nan)

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


def select_data(args):
    case = {
        'test': 'test_data',
        'training': 'training_data'
    }
    return case[args.data]


def best_counter_processor_supplier(args):
    return processors.best_counter_processor.BestCounterProcessor(args.node_count)


def simple_round_robin_supplier(args):
    return processors.simple_processor.SimpleRoundRobinProcessor(args.node_count)


def select_processor(args):
    case = {
        'simple-round-robin': simple_round_robin_supplier,
        'best-counter': best_counter_processor_supplier
    }
    select_function = case[args.processor]
    log.info('action=selecting-processor value=%s' % args.processor)
    return select_function(args)


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--processor", help="Request processor")
    parser.add_argument("-n", "--node-count", help="Node count")
    parser.add_argument("-t", "--threads", help="Thread count")
    parser.add_argument("-d", "--data", help="Data")
    args = parser.parse_args()
    log.info('action=args values="%s"' % args)
    return args


def main_wrapper():
    args = process_args()
    # processor = select_processor(args)
    data = generator.Generator(cursor=db.get_cursor(
    ), table=select_data(args), limit=30000, offset=1000)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=int(args.threads)) as executor:
    #     log.info('action=processing status=start')
    #     start_time = time.time()
    #     executor.map(processor.process, data)
    # counters_sum = sum(processor.node_counters)
    # utilization = [c*int(args.node_count)/counters_sum for c in processor.node_counters]
    # log.info('action=processing status=end time=%s' % (time.time() - start_time))
    # log.info('action=counters data=\'%s\' utilization=\'%s\' sum=%d' % (processor.node_counters, utilization, counters_sum))
    learning = regression.LinearRegression()
    learning.learn(data)
    log.info('%s' % learning.ws)


def main():
    try:
        main_wrapper()
    except Exception:
        log.info('action=end-with-exception')
        raise

if __name__ == "__main__":
    main()
