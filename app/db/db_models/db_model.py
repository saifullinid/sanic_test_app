from sqlalchemy import MetaData, Table, String, Integer, Column, Boolean, ForeignKey


metadata = MetaData()


users = Table('users', metadata,
              Column('id', Integer(), primary_key=True),
              Column('username', String(32), nullable=False, unique=True),
              Column('email', String(128), nullable=False, unique=True),
              Column('psw', String(128), nullable=False),
              Column('active_status', Boolean(), default=False),
              Column('admin_function', Boolean(), default=False),
              )

products = Table('products', metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('header', String(128), nullable=False),
                 Column('description', String(256), nullable=False),
                 Column('price', Integer(), nullable=False),
                 )

payment_accounts = Table('payment_accounts', metadata,
                         Column('id', Integer(), primary_key=True),
                         Column('balance', Integer(), nullable=False),
                         Column('user_id', Integer(), ForeignKey(users.columns.id))
                         )

transactions = Table('transactions', metadata,
                     Column('id', Integer(), primary_key=True),
                     Column('input_id', Integer(), unique=True),
                     Column('amount', Integer(), nullable=False),
                     Column('payment_accounts_id', Integer(), ForeignKey(payment_accounts.columns.id))
                     )


