def to_geojson(type='Feature', geometry=None, **kwargs):
    if geometry is None:
        geometry = {}

    res = {
        'type': type,
        'geometry': geometry
    }

    if kwargs:
        res['properties'] = {k: v for k, v in kwargs.items()}
    return res


def contains_params(request, params):
    return all(x in request.args for x in params)
