from sanic import Sanic
from sqlalchemy import insert, select, update, delete
from werkzeug.security import generate_password_hash, check_password_hash

from app.db.db_models.db_model import users, products, payment_accounts, transactions


class DBService:
    def __init__(self):
        self.db = Sanic.get_app().ctx.db

    # CHECKING
    @staticmethod
    def check_password(password_hash, psw):
        return check_password_hash(password_hash, psw)

    async def check_username(self, username):
        async with self.db.connect() as conn:
            sel = select(users).\
                where(users.c.username == username)
            user = await conn.execute(sel).first()
            if user:
                return True

    async def check_email(self, email):
        async with self.db.connect() as conn:
            sel = select(users).\
                where(users.c.email == email)
            email = await conn.execute(sel).first()
            if email:
                return True

    async def check_admin_function(self, username):
        async with self.db.connect() as conn:
            sel = select(users.c.admin_function).\
                where(users.c.username == username)
            return await conn.execute(sel).first()[0]

    async def check_payment_account(self, payment_accounts_id):
        async with self.db.connect() as conn:
            sel = select(payment_accounts).\
                where(payment_accounts.c.id == payment_accounts_id)
            payment_account = await conn.execute(sel).first()
            if payment_account:
                return True

    # ADD
    async def add_user(self, username, email, psw):
        async with self.db.begin() as conn:
            password_hash = self.set_password(psw)
            ins = insert(users).\
                values(username=username, email=email, psw=password_hash)
            await conn.execute(ins)

    async def add_payment_account(self, payment_accounts_id, balance, user_id):
        async with self.db.begin() as conn:
            ins = insert(payment_accounts).\
                value(id=payment_accounts_id, balance=balance, user_id=user_id)
            await conn.execute(ins)

    async def add_transaction(self, input_id, amount, payment_accounts_id):
        async with self.db.begin() as conn:
            ins = insert(transactions).\
                values(input_id=input_id, amount=amount, payment_accounts_id=payment_accounts_id)
            await conn.execute(ins)

    async def add_product(self, header, description, price):
        async with self.db.begin() as conn:
            ins = insert(products).\
                values(header=header, description=description, price=price)
            await conn.execute(ins)

    # SET
    @staticmethod
    def set_password(psw):
        return generate_password_hash(psw)

    async def set_active_status(self, username, status):
        async with self.db.begin() as conn:
            upd = update(users).\
                where(users.c.username == username).\
                values(active_status=status)
            await conn.execute(upd)

    async def set_balance(self, payment_accounts_id, balance):
        async with self.db.begin() as conn:
            upd = update(payment_accounts).\
                where(payment_accounts.c.id == payment_accounts_id).\
                values(balance=balance)
            await conn.execute(upd)

    async def set_product_data(self, product_id, input_data: dict):
        async with self.db.begin() as conn:
            upd = update(products).\
                where(products.c.id == product_id).\
                values(**input_data)
            await conn.execute(upd)

    async def change_product(self, product_id, header, description, price):
        async with self.db.begin() as conn:
            upd = update(products).\
                where(products.c.id == product_id).\
                values(header=header, description=description, price=price)
            await conn.execute(upd)

    # GET
    async def get_password_hash(self, username):
        async with self.db.connect() as conn:
            sel = select(users.c.psw).where(users.c.username == username)
            return await conn.execute(sel).first()[0]

    async def get_products_list(self):
        async with self.db.connect() as conn:
            sel = select(products)
            return await conn.execute(sel).fetchall()

    async def get_users_list(self):
        async with self.db.connect() as conn:
            sel = select(users)
            return await conn.execute(sel).fetchall()

    async def get_balance(self, username):
        async with self.db.connect() as conn:
            sel = select(payment_accounts.c.id, payment_accounts.c.balance).\
                select_from(users.outerjoin(payment_accounts)).\
                where(users.c.username == username)
            return await conn.execute(sel).fetchall()

    async def get_product_price(self, product_id):
        async with self.db.connect() as conn:
            sel = select(products.c.price).\
                where(products.c.id == product_id)
            return await conn.execute(sel).first()[0]

    # DELETE
    async def delete_product(self, product_id):
        async with self.db.begin() as conn:
            d = delete(products).\
                where(products.c.id == product_id)
            await conn.execute(d)
