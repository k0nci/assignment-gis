from quart import abort


def check_params(request, params):
    missing = [x not in request.args for x in params]
    if any(missing):
        abort(400)
