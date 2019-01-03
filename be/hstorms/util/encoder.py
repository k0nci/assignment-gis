import json
from datetime import datetime


class DatetimeJSONEncoder(json.JSONEncoder):

    def default(self, object_):
        if isinstance(object_, datetime):
            return object_.isoformat()
        else:
            return super().default(object_)