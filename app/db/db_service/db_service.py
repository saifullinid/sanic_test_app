from sanic import Sanic
from sqlalchemy import insert, select, update, delete
from sqlalchemy.dialects.postgresql import insert as dia_insert
from werkzeug.security import generate_password_hash, check_password_hash

from app.db.db_models.db_model import users, products, payment_accounts, transactions


class DBService:
    def __init__(self):
        self.db = Sanic.get_app().ctx.db

    # CHECKING
    async def check_password(self, username, psw):
        async with self.db.connect() as conn:
            sel = select(users.c.psw).where(users.c.username == username)
            res = await conn.execute(sel)
            password_hash = res.first()[0]
            return check_password_hash(password_hash, psw)

    async def check_username(self, username):
        async with self.db.connect() as conn:
            sel = select(users).\
                where(users.c.username == username)
            res = await conn.execute(sel)
            user = res.first()
            if user:
                return True

    async def check_email(self, email):
        async with self.db.connect() as conn:
            sel = select(users).\
                where(users.c.email == email)
            res = await conn.execute(sel)
            email = res.first()
            if email:
                return True

    async def check_product(self, product_id):
        async with self.db.connect() as conn:
            sel = select(products).\
                where(products.c.id == product_id)
            res = await conn.execute(sel)
            product = res.first()
            if product:
                return True

    async def check_admin_function(self, username):
        async with self.db.connect() as conn:
            sel = select(users.c.admin_function).\
                where(users.c.username == username)
            res = await conn.execute(sel)
            return res.first()[0]

    async def check_active_status(self, username):
        async with self.db.connect() as conn:
            sel = select(users.c.active_status).\
                where(users.c.username == username)
            res = await conn.execute(sel)
            return res.first()[0]

    async def check_payment_account(self, payment_account_id):
        async with self.db.connect() as conn:
            sel = select(payment_accounts).\
                where(payment_accounts.c.id == payment_account_id)
            res = await conn.execute(sel)
            payment_account = res.first()
            if payment_account:
                return True

    # ADD
    async def add_user(self, username, email, psw):
        async with self.db.begin() as conn:
            password_hash = self.set_password(psw)
            ins = insert(users).\
                values(username=username,
                       email=email,
                       psw=password_hash)
            await conn.execute(ins)

    async def add_payment_account(self, payment_account_id, balance, user_id):
        async with self.db.begin() as conn:
            ins = insert(payment_accounts).\
                value(id=payment_account_id,
                      balance=balance,
                      user_id=user_id)
            await conn.execute(ins)

    async def add_transaction(self,
                              payment_account_id,
                              payment_user_id,
                              input_transaction_id,
                              transaction_amount):
        async with self.db.begin() as conn:
            sel = select(payment_accounts.c.balance).\
                where(payment_accounts.c.id == payment_account_id).label('sel_balance')
            ins_1 = dia_insert(payment_accounts).\
                values(id=payment_account_id,
                       balance=transaction_amount,
                       user_id=payment_user_id).\
                on_conflict_do_update(constraint=payment_accounts.primary_key,
                                      set_={'balance': sel + transaction_amount})
            ins_2 = insert(transactions).\
                values(input_id=input_transaction_id,
                       amount=transaction_amount,
                       payment_account_id=payment_account_id)
            await conn.execute(ins_1)
            await conn.execute(ins_2)

    async def add_product(self, header, description, price):
        async with self.db.begin() as conn:
            ins = insert(products).\
                values(header=header,
                       description=description,
                       price=price)
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

    async def set_balance(self, payment_account_id, balance):
        async with self.db.begin() as conn:
            upd = update(payment_accounts).\
                where(payment_accounts.c.id == payment_account_id).\
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
                values(header=header,
                       description=description,
                       price=price)
            await conn.execute(upd)

    # GET
    async def get_products_list(self):
        async with self.db.connect() as conn:
            sel = select(products)
            res = await conn.execute(sel)
            return res.fetchall()

    async def get_users_list(self):
        async with self.db.connect() as conn:
            sel = select(users)
            res = await conn.execute(sel)
            return res.fetchall()

    async def get_balance(self, payment_account_id):
        async with self.db.connect() as conn:
            sel = select(payment_accounts.c.balance).\
                where(payment_accounts.c.id == payment_account_id)
            res = await conn.execute(sel)
            return res.first()[0]

    async def get_product_price(self, product_id):
        async with self.db.connect() as conn:
            sel = select(products.c.price).\
                where(products.c.id == product_id)
            res = await conn.execute(sel)
            return res.first()[0]

    # DELETE
    async def delete_product(self, product_id):
        async with self.db.begin() as conn:
            d = delete(products).\
                where(products.c.id == product_id)
            await conn.execute(d)
