from quart import Blueprint
from quart import jsonify

from hstorms.repository import country_r

blueprint = Blueprint('countries', __name__)


@blueprint.route('/', methods=['GET'])
async def get_countries():
    data = await country_r.find_countries()
    return jsonify(data)
