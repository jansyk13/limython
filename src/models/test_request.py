from models.request import Request
import logging as log
import sys
import unittest

log.basicConfig(stream=sys.stdout, level=log.DEBUG,
                format='%(asctime)-15s %(threadName)s %(filename)s %(levelname)s %(message)s')


class RequestTest(unittest.TestCase):

    def testClone(self):
        req = Request(1, '127.0.0.1', '30:13:57:47',
                      'GET', 'A/B/C', 'HTTP 1.1', 200, 200)
        cloned = Request.clone_with_predicted(req, 250)

        self.assertEqual(cloned.__dict__, Request(1, '127.0.0.1', '30:13:57:47',
                                                  'GET', 'A/B/C', 'HTTP 1.1', 200, 200, 250).__dict__)
