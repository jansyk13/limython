import logging as log


class DummyProcessor:

    def process(self, data):
        log.debug("hit")
        self.node_counters = None
