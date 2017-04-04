import logging as log


class BestCounterProcessor:

    def __init__(self, node_count):
        self.node_count = int(node_count)
        self.node_counters = [0] * int(node_count)

    def process(self, data):
        log.debug('action=process status=start')
        index = self.node_counters.index(min(self.node_counters))
        # adding payload_size size to counter
        self.node_counters[index] += data if data > 0 else 0
        log.debug('action=process status=end')
