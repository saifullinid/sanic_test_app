from sanic import response, Sanic
from sanic.views import HTTPMethodView
from sanic_ext import render


class MainPage(HTTPMethodView):
    async def get(self, request):
        return await render('index.html', context={'title': 'this is INDEX page'}, status=200)


class Registration(HTTPMethodView):
    async def get(self, request):
        app = Sanic.get_app()
        return await render('reg.html', context={'title': 'this is REGISTRATION page'}, status=200)

    async def post(self, request):
        app = Sanic.get_app()
        username = request.form.get('username')
        email = request.form.get('email')
        psw = request.form.get('psw')
        # TODO if check_username
        # TODO if check_email
        # if username and email: # check
        #     #TODO create_new_user
        #     #TODO send_token_to_email
        #     return response.redirect(app.url_for('MainPage'))
        # return response.redirect(app.url_for('Registration'))


class RegistrationConfirm(HTTPMethodView):
    async def get(self, request, token):
        # TODO if check_token user_status => 'active'
        pass


class Login(HTTPMethodView):
    async def get(self, request):
        return render('registration.html', context={'title': 'this is LOGIN page'}, status=200)

    async def post(self, request):
        app = Sanic.get_app()
        username = request.form.get('username')
        psw = request.form.get('psw')
        # TODO if check_username
        # TODO if check_psw
        # if username and email: # check
        #     return response.redirect(app.url_for('MainPage'))
        return response.redirect(app.url_for('Login'))


class ProductsViewer(HTTPMethodView):
    async def get(self, request):
        # TODO get request to db, get_products_list()
        pass


class BalanceViewer(HTTPMethodView):
    async def get(self, request):
        # TODO get request to db, get_balance
        pass


class ProductsBuyer(HTTPMethodView):
    async def patch(self, request, product):
        # TODO get and patch request to db,
        #  get_price(product),
        #  get_balance(username),
        #  balance -= product_price,
        #  patch_balance(balance)
        pass


class DepositMaker(HTTPMethodView):
    async def post(self, request, webhook):
        # TODO post request to db,
        #  check_signature(webhook_JSON)
        #  make_transaction(webhook_JSON)
        pass


# admin
class UsersManagement(HTTPMethodView):
    # TODO if is_admin_check(username)
    async def get(self, request):
        # TODO get_users()
        pass

    # TODO if is_admin_check(username)
    async def patch(self, request, username):
        # TODO set_user_status(username)
        pass


class ProductsManagement(HTTPMethodView):
    # TODO if is_admin_check(username)
    async def get(self, request):
        # TODO get_products_list()
        pass

    # TODO if is_admin_check(username)
    async def post(self, request, data):
        # TODO create_product(data)
        pass

    # TODO if is_admin_check(username)
    async def put(self, request, data):
        # TODO put_change_product(product_all_data)
        pass

    # TODO if is_admin_check(username)
    async def patch(self, request, data):
        # TODO patch_change_product(product_some_data)
        pass

    # TODO if is_admin_check(username)
    async def delete(self, request, data):
        # TODO delete_product(product)
        pass
