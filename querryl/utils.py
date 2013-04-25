import json

from twisted.python.failure import Failure


class FailureEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Failure):
            return {'error': obj.value.message}
