import logging as log


class SimpleRoundRobinProcessor:

    def __init__(self, node_count):
        self.node_count = int(node_count)
        self.current_node = 1
        self.predict_node_counters = [0] * int(node_count)
        self.real_node_counters = [0] * int(node_count)

    def process(self, predict, real):
        log.debug('action=process status=start')
        # select next node
        selected_node = self.current_node
        # get next node
        self.current_node += 1
        # back to first node
        if self.current_node > self.node_count:
            self.current_node = 1
        # index starts with 0
        index = selected_node - 1
        # add payload_size to counter
        self.predict_node_counters[index] += predict if predict > 0 else 0
        self.real_node_counters[index] += real if real > 0 else 0
        log.debug('action=process status=end')
