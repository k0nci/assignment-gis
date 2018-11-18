from flask_env import MetaFlaskEnv


class Configuration(metaclass=MetaFlaskEnv):
    DEBUG = True
    HSTORMSDB_URI = ''
