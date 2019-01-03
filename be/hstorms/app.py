import asyncpg
from quart import Quart
from quart_cors import cors

from hstorms.config import Configuration
from hstorms.util.encoder import DatetimeJSONEncoder


def create_app():
    app = Quart(__name__)
    app.config.from_object(Configuration)

    @app.before_first_request
    async def create_db():
        app.pool = await asyncpg.create_pool(Configuration.HSTORMSDB_URI,
                                             max_size=20)

    register_blueprints(app)
    register_extensions(app)
    register_encoders(app)

    @app.route('/')
    async def root():
        return 'hstorms-api'

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
