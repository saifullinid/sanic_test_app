from sanic import Sanic


from app.routes.routes import launch_routes
from config import AppConfig, launch_connections

app = Sanic(__name__)
app.update_config(AppConfig)
app.extend(config={'TEMPLATING_PATH_TO_TEMPLATES': app.config['TEMPLATING_PATH_TO_TEMPLATES']})


def init():
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=app.config.DEBUG,
        auto_reload=app.config.AUTO_RELOAD,
    )


if __name__ == '__main__':
    init()
if __name__ == '__mp_main__':
    launch_connections(app)
    launch_routes(app)










