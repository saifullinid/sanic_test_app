from sanic.response import text


def launch_routes(app):
    @app.get('/')
    def checker(request):
        return text('hello')
