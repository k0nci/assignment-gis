from quart import Blueprint
from quart import abort
from quart import jsonify
from quart import request

from repository import hurricane_r

blueprint = Blueprint('main', __name__)


@blueprint.route('/point', methods=['GET'])
async def get_closest():
    if any(x not in request.args for x in ['lat', 'lon']):
        abort(400)

    point = {
        'lat': float(request.args['lat']),
        'lon': float(request.args['lon'])
    }

    data = await hurricane_r.find_closest(point)
    return jsonify(data)
