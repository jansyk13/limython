import json
import logging as log
import threading
import time


class BestCounterProcessor:

    def __init__(self, node_count):
        self.node_count = int(node_count)
        self.lock = threading.Lock()
        self.node_counters = [0] * int(node_count)

    def process(self, request):
        log.debug('action=process status=start id=%s data="%s"' %
                  (request.id, json.dumps(request.__dict__)))
        try:
            # get lock
            # using only one lock because min function needs lock on all of
            # counters
            self.lock.acquire()
            # getting index of counter with lowest value
            index = self.node_counters.index(min(self.node_counters))
            # adding payload size to counter
            self.node_counters[index] += request.payload_size
            log.debug('action=payload-processing id=%s value=%s' %
                      (request.id, request.payload_size))
        except Exception as ex:
            log.exception('action=payload-processing status=error')
        finally:
            # release lock
            self.lock.release()
        log.debug('action=process status=end id=%s' % request.id)
