from quart import Blueprint
from quart import abort
from quart import jsonify
from quart import request

from repository import hurricane_r
from util import contains_params

blueprint = Blueprint('hurricanes', __name__)


@blueprint.route('/point', methods=['GET'])
async def get_by_point():
    required_params = ['lat', 'lon']
    if not contains_params(request, required_params):
        abort(400)

    point = {
        'lat': float(request.args['lat']),
        'lon': float(request.args['lon'])
    }

    if 'distance' in request.args and float(request.args['distance']) > 0:
        distance = float(request.args['distance'])
        data = await hurricane_r.find_dwithin(point, distance)
        return jsonify(data)

    data = await hurricane_r.find_closest(point)
    return jsonify(data)


@blueprint.route('/occurrence', methods=['GET'])
async def count_occurrence_for_country():
    required_params = ['country_id']
    if not contains_params(request, required_params):
        abort(400)

    country_id = int(request.args['country_id'])
    data = await hurricane_r.count_occurrence_in_region(country_id)
    if not data['features']:
        data = await hurricane_r.count_occurrence_in_country(country_id)

    return jsonify(data)
