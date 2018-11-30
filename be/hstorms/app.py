import asyncpg
from quart import Quart
from quart_cors import cors

from config import Configuration
from util import DatetimeJSONEncoder


def create_app():
    app = Quart(__name__)
    app.config.from_object(Configuration)

    @app.before_first_request
    async def create_db():
        dsn = Configuration.HSTORMSDB_URI
        app.pool = await asyncpg.create_pool(dsn, max_size=20)

    register_blueprints(app)
    register_extensions(app)
    register_encoders(app)
    return app


def register_blueprints(app):
    from .controller import hurricane_c
    from .controller import country_c
    app.register_blueprint(hurricane_c.blueprint, url_prefix='/hurricanes')
    app.register_blueprint(country_c.blueprint, url_prefix='/countries')


def register_extensions(app):
    cors(app)


def register_encoders(app):
    app.json_encoder = DatetimeJSONEncoder
