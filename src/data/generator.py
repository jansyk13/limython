from models.request import Request
import gc
import logging as log

class Generator:
    def __init__(self, cursor, table, offset, limit):
        self.cursor = cursor
        self.limit = limit
        self.offset = offset
        self.table = table

    def __iter__(self):
        _id = 1
        while True:
            _select = self._create_select(_id)
            self.cursor.execute(_select)
            if not self.cursor.rowcount:
                break
            for row in self.cursor.fetchall():
                yield Request(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            gc.collect()
            log.info('action=gc-called')
            if _id > self.limit: break
            _id += self.offset

    def _create_select(self, id):
        return "SELECT id, source, time_stamp, method, url, protocol, status, payload_size FROM %s WHERE id>=%d ORDER BY id ASC LIMIT %d" % (self.table, id, self.offset)
