import logging as log


class SimpleRoundRobinProcessor:

    def __init__(self, node_count):
        self.node_count = int(node_count)
        self.current_node = 1
        self.node_counters = [0] * int(node_count)

    def process(self, data):
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
        self.node_counters[index] += data
        log.debug('action=process status=end')
