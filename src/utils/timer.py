import logging as log
import time


def start():
    return time.time()


def stop(t):
    log.info("action=timer value=%s" % (time.time() - t))
