import json


def to_geojson(geometry=None, **kwargs):
    if geometry is None:
        geometry = {}
    elif isinstance(geometry, str):
        geometry = json.loads(geometry)

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
