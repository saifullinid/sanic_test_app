import jwt
import json

from sanic import response, Sanic, text
from sanic.views import HTTPMethodView
from sanic_ext import render

from app.app_service.app_service import AppService, get_activation_link
from app.app_service.auth_module import protected, protected_admin
from app.app_service.send_email import send_email


class MainPage(HTTPMethodView):
    async def get(self, request):
        title = 'this is INDEX page'
        msg = ''
        if request.args.get('msg'):
            msg = request.args.get('msg')
        return await render('index.html',
                            context={'title': title,
                                     'msg': msg},
                            status=200)


class Registration(HTTPMethodView):
    async def get(self, request):
        return await render('reg.html', context={'title': 'this is REGISTRATION page'}, status=200)

    async def post(self, request):
        app = Sanic.get_app()
        app_service = AppService()

        username = request.json.get('username')
        email = request.json.get('email')
        psw = request.json.get('psw')

        res_from_service = await app_service.registration(username, email, psw)
        if res_from_service.get('error'):
            msg = res_from_service.get('error')
            return await render('reg.html',
                                context={'title': 'this is REGISTRATION page',
                                         'flash': msg},
                                status=200)

        activation_link = get_activation_link(request, username)
        message_title = 'activation link'
        send_email(email, activation_link, message_title)

        msg = 'You have been sent a link to activate your profile'
        return response.redirect(app.url_for('MainPage', msg=msg))


class RegistrationConfirm(HTTPMethodView):
    async def get(self, request, token):
        app = Sanic.get_app()
        app_service = AppService()
        res_from_service = await app_service.reg_confirm(request, token)
        if res_from_service.get('error'):
            msg = res_from_service.get('error')
            return response.redirect(app.url_for('MainPage', msg=msg))

        request.ctx.session['active_status'] = True
        msg = res_from_service.get('data')
        return response.redirect(app.url_for('MainPage', msg=msg))


class Login(HTTPMethodView):
    async def get(self, request):
        app = Sanic.get_app()
        if request.ctx.session.get('username'):
            return response.redirect(app.url_for('MainPage'))
        return await render('login.html', context={'title': 'this is LOGIN page'}, status=200)

    async def post(self, request):
        app_service = AppService()
        username = request.json.get('username')
        psw = request.json.get('psw')

        res_from_service = await app_service.login(username, psw)
        if res_from_service.get('error'):
            msg = res_from_service.get('error')
            return await render('login.html',
                                context={'title': 'this is LOGIN page',
                                         'msg': msg},
                                status=200)

        res_from_service = await app_service.check_active_status(username)
        if res_from_service.get('data'):
            request.ctx.session['active_status'] = True

        res_from_service = await app_service.check_admin_function(username)
        if res_from_service.get('data'):
            request.ctx.session['admin_function'] = True

        request.ctx.session['username'] = username
        token = jwt.encode({'username': username}, request.app.config['SECRET_KEY'])
        return text(token)


class ProductsViewer(HTTPMethodView):
    decorators = [protected]

    async def get(self, request):
        app_service = AppService()
        res_from_service = await app_service.get_products_list()
        return response.json(res_from_service)


class BalanceViewer(HTTPMethodView):
    decorators = [protected]

    async def get(self, request):
        app_service = AppService()
        payment_account_id = request.json.get('payment_account_id')
        res_from_service = await app_service.get_balance(payment_account_id)

        return response.json(res_from_service)


class ProductsBuyer(HTTPMethodView):
    decorators = [protected]

    async def patch(self, request, product_id):
        app_service = AppService()
        payment_account_id = request.json.get('payment_account_id')
        res_from_service = await app_service.buy_product(product_id, payment_account_id)

        return response.json(res_from_service)


class DepositMaker(HTTPMethodView):
    decorators = [protected]

    async def post(self, request, webhook):
        app_service = AppService()
        webhook = json.loads(webhook)
        input_signature = webhook['signature']
        input_transaction_id = webhook['transaction_id']
        user_id = webhook['user_id']
        payment_account_id = webhook['bill_id']
        amount = webhook['amount']
        res_from_service = await app_service.make_deposit(input_signature,
                                                          input_transaction_id,
                                                          user_id,
                                                          payment_account_id,
                                                          amount)
        return response.json(res_from_service)


# admin
class UsersManagement(HTTPMethodView):
    decorators = [protected_admin]

    async def get(self, request):
        app_service = AppService()
        res_from_service = await app_service.get_users_list()

        return response.json(res_from_service)

    async def patch(self, request):
        app_service = AppService()
        username = request.json.get('username')
        status = request.json.get('status')
        res_from_service = await app_service.set_active_status(username, status)

        return response.json(res_from_service)


class ProductsManagement(HTTPMethodView):
    decorators = [protected_admin]

    async def get(self, request):
        app_service = AppService()
        res_from_service = await app_service.get_products_list()

        return response.json(res_from_service)

    async def post(self, request):
        app_service = AppService()
        header = request.json.get('header')
        description = request.json.get('description')
        price = request.json.get('price')

        res_from_service = await app_service.add_product(header, description, price)

        return response.json(res_from_service)

    async def put(self, request):
        app_service = AppService()
        product_id = request.json.get('product_id')
        header = request.json.get('header')
        description = request.json.get('description')
        price = request.json.get('price')

        res_from_service = await app_service.change_product(product_id, header, description, price)

        return response.json(res_from_service)

    async def patch(self, request):
        app_service = AppService()
        product_id = request.json.get('product_id')
        input_data = request.json.get('input_data')

        res_from_service = await app_service.set_product_some_data(product_id, input_data)

        return response.json(res_from_service)

    async def delete(self, request):
        app_service = AppService()
        product_id = request.json.get('product_id')

        res_from_service = await app_service.delete_product(product_id)

        return response.json(res_from_service)
