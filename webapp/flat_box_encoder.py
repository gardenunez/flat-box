from decimal import Decimal
from flask.json import JSONEncoder


class FlatBoxJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return JSONEncoder.default(obj)