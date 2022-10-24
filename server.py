from sanic import Sanic
from app.routes.routes import launch_routes

app = Sanic(__name__)


launch_routes(app)
