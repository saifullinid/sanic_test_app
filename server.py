from sanic import Sanic
from app.routes.routes import launch_routes

print('hello')
app = Sanic(__name__)
app.extend(config={'TEMPLATING_PATH_TO_TEMPLATES': './app/templates'})


launch_routes(app)
