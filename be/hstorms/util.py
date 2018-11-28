def to_geojson(geometry=None, **kwargs):
    if geometry is None:
        geometry = {}
    # TODO load geometry if not json

    return {
        'type': 'Feature',
        'geometry': geometry,
        'properties': {k: v for k, v in kwargs.items()}
    }


def to_geojson_collection(features=None):
    return {
        'type': 'FeatureCollection',
        'features': features
    }


def contains_params(request, params):
    return all(x in request.args for x in params)
