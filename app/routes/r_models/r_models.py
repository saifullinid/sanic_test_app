from sanic.views import HTTPMethodView


class MainPage(HTTPMethodView):
    async def get(self):
        pass


class Registration(HTTPMethodView):
    async def get(self):
        pass

    async def post(self):
        pass


class RegistrationConfirm(HTTPMethodView):
    async def get(self):
        pass


class Login(HTTPMethodView):
    async def get(self):
        pass

    async def post(self):
        pass


class ProductsViewer(HTTPMethodView):
    async def get(self):
        pass


class ProductsBuyer(HTTPMethodView):
    async def post(self):
        pass


class BalanceViewer(HTTPMethodView):
    async def get(self):
        pass


class DepositMaker(HTTPMethodView):
    async def post(self):
        pass


# admin
class UsersManagement(HTTPMethodView):
    async def get(self):
        pass

    async def patch(self):
        pass


class ProductsManagement(HTTPMethodView):
    async def get(self):
        pass

    async def post(self):
        pass

    async def put(self):
        pass

    async def patch(self):
        pass

    async def delete(self):
        pass
