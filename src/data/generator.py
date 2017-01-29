from models.request import Request

class Generator:
    def __init__(self, cursor, table, offset, limit):
        self.cursor = cursor
        self.limit = limit
        self.offset = offset
        self.table = table

    def __iter__(self):
        _id = 1
        while True:
            # creating SELECT
            _select = self._create_select(_id)
            # DB call
            self.cursor.execute(_select)
            if not self.cursor.rowcount:
                # no more records
                break
            for row in self.cursor.fetchall():
                yield Request(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            # over limit -> end
            if _id > self.limit: break
            # next
            _id += self.offset

    def _create_select(self, id):
        # id + limit paging is faster than standard limit + offset
        # full scan of indexed column instead of full scan of a whole table
        return "SELECT id, source, time_stamp, method, url, protocol, status, payload_size FROM %s WHERE id>=%d ORDER BY id ASC LIMIT %d" % (self.table, id, self.offset)
