from quart import json
from datetime import datetime


def to_geojson(geometry=None, **kwargs):
    if geometry is None:
        geometry = {}
    # TODO load geometry if not json

    return {
        'type': 'Feature',
        'geometry': geometry,
        'properties': {k: v for k, v in kwargs.items()}
    }


def to_geojson_collection(features=None, **kwargs):
    res = {
        'type': 'FeatureCollection',
        'features': features
    }

    if kwargs:
        res['properties'] = {k: v for k, v in kwargs.items()}
    return res


def contains_params(request, params):
    return all(x in request.args for x in params)


class DatetimeJSONEncoder(json.JSONEncoder):

    def default(self, object_):
        if isinstance(object_, datetime):
            return object_.isoformat()
        else:
            return super().default(object_)
