import copy

# model class for Request
class Request:

    def __init__(self, id, source, time_stamp, method, url, protocol, status, payload_size, predicted_payload_size=None):
        self.id = id
        self.source = source
        self.time_stamp = time_stamp
        self.method = method
        self.url = url
        self.protocol = protocol
        self.status = int(status)
        self.payload_size = payload_size if payload_size is not None else 0
        self.predicted_payload_size = predicted_payload_size

    @classmethod
    def clone_with_predicted(cls, request, predicted_payload_size):
        _request = copy.deepcopy(request)
        return cls(_request.id, _request.source, _request.time_stamp,
                   _request.method, _request.url, _request.protocol,
                   _request.status, _request.payload_size, predicted_payload_size)
