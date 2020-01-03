import os

from yarl import URL

basedir = os.path.abspath(os.path.dirname(__file__))

HASH_METHOD = os.getenv('HASH_METHOD', 'sha256')

# start region DATABASE:
DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA", "postgresql")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "sapi")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "sapi")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", 5432)
DATABASE_NAME = os.getenv("DATABASE_NAME", "serverless_api")
DATABASE_URL = URL.build(
    scheme=DATABASE_SCHEMA, host=DATABASE_HOST, port=int(DATABASE_PORT),
    user=DATABASE_USERNAME, password=DATABASE_PASSWORD,
    path=f"/{DATABASE_NAME}",
)
# endregion

# Start region Config


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'dev'
    PASSWORD_RESET_SECRET_KEY = 'password-reset'
    SQLALCHEMY_DATABASE_URI = f'{DATABASE_URL}'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = os.getenv('DEV_DEBUG', False)
    ENV='development'


# endregion