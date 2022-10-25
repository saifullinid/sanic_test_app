from databases import Database


def launch_database(app):
    app.ctx.db = Database(app.config['DB_URI'])

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        await app.ctx.db.connect()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        await app.ctx.db.disconnect()
