import logging as log


class DummyProcessor:

    def __init__(self):
        log.info("action=init")
        self.node_counters = []

    def process(self, data):
        log.debug("hit")
