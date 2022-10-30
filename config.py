from sanic import Sanic
from asyncio import Queue
from sanic.config import Config
from sanic_session import Session
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.db_service.db_service import DBService


class AppConfig(Config):
    DEBUG: bool = True
    HOST: str = '127.0.0.1'
    PORT: int = 8000
    SECRET_KEY = 'some_secret_key'
    TEMPLATING_PATH_TO_TEMPLATES: str = './app/templates'
    AUTO_RELOAD: bool = True
    DB_URI: str = 'postgresql+asyncpg://sid:12345@localhost/sanic_db'


def launch_connections(app):
    @app.listener('after_server_start')
    def connect_to_db(app, loop):
        app.ctx.queue = Queue(loop=loop, maxsize=100)
        app.ctx.processed_data_dict = {}
        app.ctx.event = {}
        Session(app)
        app.ctx.db = create_async_engine(app.config['DB_URI'],
                                         pool_size=100,
                                         max_overflow=10,
                                         )
        app.ctx.db_service = DBService()

        [app.add_task(use_worker()) for _ in range(5)]

    @app.listener('after_server_stop')
    def disconnect_from_db(*args, **kwargs):
        app.ctx.db.dispose()


async def use_worker():
    while True:
        app = Sanic.get_app()
        queue = app.ctx.queue
        processed_data_dict = app.ctx.processed_data_dict
        db_service = app.ctx.db_service
        method, data, trigger = await queue.get()
        processed_data = await getattr(db_service, method)(*data)
        if trigger:
            processed_data_dict[f'{method}_{data}'] = processed_data
            event = app.ctx.event[f'{method}_{data}']
            event.set()
        queue.task_done()
