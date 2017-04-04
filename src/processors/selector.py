import logging as log
import processors.simple_processor
import processors.best_counter_processor


def best_counter_processor_supplier(args):
    return processors.best_counter_processor.BestCounterProcessor(args.node_count)


def simple_round_robin_supplier(args):
    return processors.simple_processor.SimpleRoundRobinProcessor(args.node_count)


def select_processor_supplier(args):
    case = {
        'simple-round-robin': simple_round_robin_supplier,
        'best-counter': best_counter_processor_supplier,
    }
    select_function = case[args.processor]
    log.info('action=selecting-processor value=%s' % args.processor)
    return select_function


def select_processor(args):
    select_function = select_processor_supplier(args)
    return select_function(args)
