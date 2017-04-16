import logging as log


class BestCounterProcessor:

    def __init__(self, node_count):
        self.node_count = int(node_count)
        self.predict_node_counters = [0] * int(node_count)
        self.real_node_counters = [0] * int(node_count)

    def process(self, predict, real):
        log.debug('action=process status=start')
        index = self.predict_node_counters.index(min(self.predict_node_counters))
        # adding payload_size size to counter
        self.predict_node_counters[index] += predict if predict > 0 else 0
        self.real_node_counters[index] += real if real > 0 else 0
        log.debug('action=process status=end')
