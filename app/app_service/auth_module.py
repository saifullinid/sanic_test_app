import jwt

from functools import wraps
from sanic import response, Sanic


def check_token(request):
    if not request.token:
        return False
    try:
        jwt.decode(
            request.token, request.app.config['SECRET_KEY'], algorithms=['HS256']
        )
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated and request.ctx.session['active_status']:
                res = await f(request, *args, **kwargs)
                return res
            else:
                app = Sanic.get_app()
                return response.redirect(app.url_for('Login'))

        return decorated_function
    return decorator(wrapped)


def protected_admin(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            app = Sanic.get_app()
            is_authenticated = check_token(request)

            if is_authenticated and request.ctx.session.get('active_status'):
                if not request.ctx.session.get('admin_function'):
                    return response.redirect(app.url_for('MainPage'))
                res = await f(request, *args, **kwargs)
                return res
            else:
                return response.redirect(app.url_for('Login'))

        return decorated_function
    return decorator(wrapped)
