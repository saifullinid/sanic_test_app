from app.routes.r_models import r_models as rm


def launch_routes(app):
    print('IN launch_routes')
    app.add_route(rm.MainPage.as_view(),
                  '/')
    app.add_route(rm.Registration.as_view(),
                  '/reg')
    app.add_route(rm.RegistrationConfirm.as_view(),
                  '/reg_confirm/<token>')
    app.add_route(rm.Login.as_view(),
                  '/login')
    app.add_route(rm.ProductsViewer.as_view(),
                  '/get_products_list')
    app.add_route(rm.BalanceViewer.as_view(),
                  '/get_balance')
    app.add_route(rm.ProductsBuyer.as_view(),
                  '/buy/<product>')
    app.add_route(rm.DepositMaker.as_view(),
                  '/payment/<webhook>')
    app.add_route(rm.UsersManagement.as_view(),
                  '/admin/user/<username>')
    app.add_route(rm.ProductsManagement.as_view(),
                  '/admin/product/<data>')
