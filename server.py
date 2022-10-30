from sanic import Sanic


from app.routes.routes import launch_routes
from config import AppConfig, launch_connections

app = Sanic(__name__)
app.update_config(AppConfig)
app.extend(config={'TEMPLATING_PATH_TO_TEMPLATES': app.config['TEMPLATING_PATH_TO_TEMPLATES']})


def init():
    launch_connections(app)
    launch_routes(app)


init()











