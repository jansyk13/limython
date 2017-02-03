# model class for Request
class Request:

    def __init__(self, id, source, time_stamp, method, url, protocol, status, payload_size):
        self.id = id
        self.source = source
        self.time_stamp = time_stamp
        self.method = method
        self.url = url
        self.protocol = protocol
        self.status = int(status)
        self.payload_size = payload_size if payload_size is not None else 0
