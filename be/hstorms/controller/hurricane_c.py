from quart import Blueprint
from quart import jsonify
from quart import request

from hstorms.repository import hurricane_r
from hstorms.util import check_params

blueprint = Blueprint('hurricanes', __name__)


@blueprint.route('/point', methods=['GET'])
async def get_by_point():
    required_params = ['lat', 'lon']
    check_params(request, required_params)

    point = {
        'lat': float(request.args['lat']),
        'lon': float(request.args['lon'])
    }
    year = int(request.args['year']) if 'year' in request.args else None

    if 'distance' in request.args and float(request.args['distance']) > 0:
        distance = float(request.args['distance'])
        data = await hurricane_r.find_dwithin(point, distance, year)
        return jsonify(data)

    data = await hurricane_r.find_closest(point, year)
    return jsonify(data)


@blueprint.route('/occurrence', methods=['GET'])
async def count_occurrence_for_country():
    required_params = ['countryId']
    check_params(request, required_params)

    country_id = int(request.args['countryId'])
    data = await hurricane_r.count_occurrence_in_region(country_id)
    if not data['features']:
        data = await hurricane_r.count_occurrence_in_country(country_id)

    return jsonify(data)


@blueprint.route('/<hurricane_id>/info', methods=['GET'])
async def get_hurricane_info(hurricane_id):
    hurricane_id = int(hurricane_id)

    data = await hurricane_r.get_hurricane_info(hurricane_id)
    return jsonify(data)
