import jwt
import random
import string

from sanic import Sanic
from asyncio import Event
from Crypto.Hash import SHA1


class AppService:
    def __init__(self):
        self.app = Sanic.get_app()
        self.queue = self.app.ctx.queue
        self.processed_data_dict = self.app.ctx.processed_data_dict

    async def registration(self, username, email, psw):
        queue = self.queue

        check_username = await self.check_username(username)
        if not check_username:
            return {'error': 'username not found'}

        check_email = await self.check_email(email)
        if check_email:
            return {'error': 'this email is already taken'}

        # ADD_USER_
        await queue.put(('add_user', (username, email, psw), False))

        return {'data': 'successful registration'}

    async def reg_confirm(self, request, token):
        app = self.app
        queue = self.queue

        if not request.ctx.session['activation_token'] == token:
            return {'error': 'invalid activation token'}

        username = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['username']
        set_active_status_data = (username, True)

        await queue.put(('set_active_status', set_active_status_data, False))

        return {'data': 'successful activation'}

    async def login(self, username, psw):
        check_username = await self.check_username(username)
        if not check_username:
            return {'error': 'username not found'}

        check_psw = await self.check_password(username, psw)
        if not check_psw:
            return {'error': 'incorrect password'}

        return {'data': 'successful authorization'}

    async def buy_product(self, product_id, payment_account_id):
        check_product = await self.check_product(product_id)
        if not check_product:
            return {'error': 'product not found'}

        payment_account = await self.check_payment_account(payment_account_id)
        if not payment_account:
            return {'error': 'payment account not found'}

        product_price = await self.get_product_price(product_id)

        balance = await self.get_balance(payment_account_id)

        balance = balance - product_price
        await self.set_balance(payment_account_id, balance)

        return {'data': 'purchase completed'}

    async def make_deposit(self,
                           input_signature,
                           input_transaction_id,
                           user_id,
                           payment_account_id,
                           amount):
        app = self.app
        queue = self.queue

        signature = SHA1.new()
        signature.update(f'{app.config["SECRET_KEY"]}:{input_transaction_id}:{user_id}:{payment_account_id}:{amount}'.encode())

        if signature.hexdigest() != input_signature:
            return {'error': 'bad signature'}
        add_transaction_data = (payment_account_id, user_id, input_transaction_id, amount)

        await queue.put(('add_transaction', add_transaction_data, False))

        return {'data': 'successful account replenishment'}

    async def add_product(self, header, description, price):
        queue = self.queue

        add_product_data = (header, description, price)

        await queue.put(('add_product', add_product_data, False))

        return {'data': 'product created'}

    async def change_product(self, product_id, header, description, price):
        queue = self.queue

        add_product_data = (product_id, header, description, price)

        await queue.put(('change_product', add_product_data, False))

        return {'data': 'product changed'}

    async def delete_product(self, product_id):
        queue = self.queue

        delete_product_data = (product_id,)

        await queue.put(('delete_product', delete_product_data, False))

        return {'data': 'product deleted'}

    async def get_products_list(self):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        get_products_list_data = ()

        key_get_products_list = f'get_products_list_{get_products_list_data}'
        app.ctx.event[key_get_products_list] = Event()

        await queue.put(('get_products_list', get_products_list_data, True))
        await app.ctx.event[key_get_products_list].wait()
        app.ctx.event.pop(key_get_products_list)
        products_list = processed_data_dict.pop(key_get_products_list)

        return products_list

    async def get_user_balance(self, payment_account_id):
        payment_account = await self.check_payment_account(payment_account_id)
        if not payment_account:
            return {'error': 'payment account not found'}

        balance = await self.get_balance(payment_account_id)
        return balance

    async def get_balance(self, payment_account_id):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        get_balance_data = (payment_account_id,)

        key_get_balance = f'get_balance_{get_balance_data}'
        app.ctx.event[key_get_balance] = Event()

        await queue.put(('get_balance', get_balance_data, True))
        await app.ctx.event[key_get_balance].wait()
        app.ctx.event.pop(key_get_balance)
        balance = processed_data_dict.pop(key_get_balance)
        return balance

    async def get_product_price(self, product_id):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        get_product_price_data = (product_id,)

        key_get_product_price = f'get_product_price_{get_product_price_data}'
        app.ctx.event[key_get_product_price] = Event()
        await queue.put(('get_product_price', get_product_price_data, True))

        await app.ctx.event[key_get_product_price].wait()
        app.ctx.event.pop(key_get_product_price)
        product_price = processed_data_dict.pop(key_get_product_price)
        return product_price

    async def get_users_list(self):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        get_users_list_data = ()

        key_get_users_list = f'get_users_list_{get_users_list_data}'
        app.ctx.event[key_get_users_list] = Event()

        await queue.put(('get_users_list', get_users_list_data, True))
        await app.ctx.event[key_get_users_list].wait()
        app.ctx.event.pop(key_get_users_list)
        users_list = processed_data_dict.pop(key_get_users_list)
        return users_list

    async def set_balance(self, payment_account_id, balance):
        app = self.app
        queue = self.queue

        set_balance_data = (payment_account_id, balance)

        key_set_balance = f'set_balance_{set_balance_data}'
        app.ctx.event[key_set_balance] = Event()
        await queue.put(('set_balance', set_balance_data, False))

    async def set_active_status(self, username, status):
        queue = self.queue

        check_username = self.check_username(username)
        if not check_username:
            return {'error': 'username not found'}

        # SET_ACTIVE_STATUS_
        set_active_status_data = (username, status)

        await queue.put(('set_active_status', set_active_status_data, False))
        return {'data': 'active status changed'}

    async def set_product_some_data(self, product_id, input_data: dict):
        queue = self.queue

        set_product_data = (product_id, input_data)

        await queue.put(('set_product_data', set_product_data, False))

        return {'data': 'product data changed'}

    async def check_username(self, username):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        check_username_data = (username,)

        key_check_username = f'check_username_{check_username_data}'
        app.ctx.event[key_check_username] = Event()
        await queue.put(('check_username', check_username_data, True))

        await app.ctx.event[key_check_username].wait()
        app.ctx.event.pop(key_check_username)
        check_username = processed_data_dict.pop(key_check_username)
        return check_username

    async def check_email(self, email):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        check_email_data = (email,)

        key_check_email = f'check_email_{check_email_data}'
        app.ctx.event[key_check_email] = Event()
        await queue.put(('check_email', check_email_data, True))

        await app.ctx.event[key_check_email].wait()
        app.ctx.event.pop(key_check_email)
        check_email = processed_data_dict.pop(key_check_email)
        return check_email

    async def check_password(self, username, psw):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        check_psw_data = (username, psw)

        key_check_psw = f'check_password_{check_psw_data}'
        app.ctx.event[key_check_psw] = Event()
        await queue.put(('check_password', check_psw_data, True))

        await app.ctx.event[key_check_psw].wait()
        app.ctx.event.pop(key_check_psw)
        check_psw = processed_data_dict.pop(key_check_psw)
        return check_psw

    async def check_payment_account(self, payment_account_id):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        check_payment_account_data = (payment_account_id,)

        key_check_payment_account = f'check_payment_account_{check_payment_account_data}'
        app.ctx.event[key_check_payment_account] = Event()
        await queue.put(('check_payment_account', check_payment_account_data, True))

        await app.ctx.event[key_check_payment_account].wait()
        app.ctx.event.pop(key_check_payment_account)
        payment_account = processed_data_dict.pop(key_check_payment_account)

        return payment_account

    async def check_active_status(self, username):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        check_active_status_data = (username,)
        key_active_status = f'check_active_status_{check_active_status_data}'
        app.ctx.event[key_active_status] = Event()
        await queue.put(('check_active_status', check_active_status_data, True))

        await app.ctx.event[key_active_status].wait()
        app.ctx.event.pop(key_active_status)
        active_status = processed_data_dict.pop(key_active_status)

        return {'data': active_status}

    async def check_admin_function(self, username):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        check_admin_function_data = (username,)
        key_check_admin_function = f'check_admin_function_{check_admin_function_data}'
        app.ctx.event[key_check_admin_function] = Event()
        await queue.put(('check_admin_function', check_admin_function_data, True))

        await app.ctx.event[key_check_admin_function].wait()
        app.ctx.event.pop(key_check_admin_function)
        admin_function = processed_data_dict.pop(key_check_admin_function)

        return {'data': admin_function}

    async def check_product(self, product_id):
        app = self.app
        queue = self.queue
        processed_data_dict = self.processed_data_dict

        check_product_data = (product_id,)

        key_check_product = f'check_product_{check_product_data}'
        app.ctx.event[key_check_product] = Event()
        await queue.put(('check_product', check_product_data, True))

        await app.ctx.event[key_check_product].wait()
        app.ctx.event.pop(key_check_product)
        check_product = processed_data_dict.pop(key_check_product)
        return check_product


def get_random_string(length):
    letters = string.ascii_uppercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def get_activation_link(request, username):
    app = Sanic.get_app()
    data = {'username': username, 'string': get_random_string(20)}
    token = jwt.encode(data, app.config['SECRET_KEY'], algorithm='HS256')
    request.ctx.session['activation_token'] = token
    msg = f'''<a href="{app.url_for('RegistrationConfirm', token=token)}">/{token}</a>'''
    return msg
