# Object representing node in tree
import copy
import json
import logging as log


class Node():

    def __init__(self, feature, value, left_child, right_child):
        self.feature = feature
        self.value = value
        self.left_child = left_child
        self.right_child = right_child

    @classmethod
    def clone(cls, node):
        _node = copy.deepcopy(node)
        return cls(_node.feature, _node.value,
                   _node.left_child, _node.right_child)

    @classmethod
    def only_value(cls, value):
        return cls(None, value, None, None)

    def to_json(self, indent=None):
        return json.dumps(self, default=lambda o: _resolve_dump(o), indent=indent)

    def apply(self, request_matrix):
        log.debug('action=apply self=%s request_matrix=%s' % (self.to_json(), request_matrix))
        if self.feature is None:
            return self.value
        if request_matrix[self.feature-1] > self.value:
            return self.left_child.apply(request_matrix)
        else:
            return self.right_child.apply(request_matrix)


def _resolve_dump(_object):
    if hasattr(_object, '__dict__'):
        return _object.__dict__
    else:
        return str(_object)
