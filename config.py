from sanic.config import Config


class AppConfig(Config):
    DEBUG: bool = True
    HOST: str = '127.0.0.1'
    PORT: int = 8000
    TEMPLATING_PATH_TO_TEMPLATES: str = './app/templates'
    AUTO_RELOAD: bool = True
    DB_URI: str = 'postgresql://sid:12345@localhost/sanic_db'
