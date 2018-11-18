from quart import Blueprint
from quart import jsonify

from repository import hurricane_r

blueprint = Blueprint('main', __name__)


@blueprint.route('', methods=['GET'])
async def get_all():
    data = await hurricane_r.find_all()
    return jsonify(data)
