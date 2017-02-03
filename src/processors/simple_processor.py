import threading
import time
import json
import logging as log


class SimpleRoundRobinProcessor:

    def __init__(self, node_count):
        self.node_count = int(node_count)
        self.lock = threading.Lock()
        self.current_node = 1
        self.node_locks = [threading.Lock()] * int(node_count)
        self.node_counters = [0] * int(node_count)

    def process(self, request):
        log.info('action=process status=start id=%s data="%s"' %
                 (request.id, json.dumps(request.__dict__)))
        # select next node while using lock to make this thread safe
        try:
            # get lock
            self.lock.acquire()
            selected_node = self.current_node
            # get next node
            self.current_node += 1
            # back to first node
            if self.current_node > self.node_count:
                self.current_node = 1
        except Exception as ex:
            log.exception('action=round-robin status=error')
        finally:
            # release lock
            self.lock.release()
        # index starts with 0
        index = selected_node - 1
        try:
            # get lock - counter specific
            self.node_locks[index].acquire()
            log.info('action=payload-processing status=start id=%s value=%s' %
                     (request.id, request.payload_size))
            # add payload size to counter
            self.node_counters[index] += request.payload_size
            log.info('action=payload-processing status=end id=%s' % request.id)
        except Exception as ex:
            log.exception('action=payload-processing status=error')
        finally:
            # release lock - counter specific
            self.node_locks[index].release()
        log.info('action=process status=end id=%s' % request.id)
