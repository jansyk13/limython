import logging as log


class DummyProcessor:

    def __init__(self):
        log.info("action=init")
        self.real_node_counters = []
        self.predict_node_counters = []

    def process(self, predict, real):
        log.debug("hit")
