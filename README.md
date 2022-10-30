# sanic_test

Запуск через командную строку:


Изменение метода запуска:
для запуска через 'if __name__ == '__main__' заменить в server.py

    init()

на

    def init():
        app.run()
    
    if __name__ == '__main__':
        init()
    if __name__ == '__mp_main__':
        launch_connections(app)
        launch_routes(app)

в 'app.run()' прописать необходимые настройки, например:

    app.run(
        host='127.0.0.1',
        port=8000,
        debug=app.config.DEBUG,
        auto_reload=app.config.AUTO_RELOAD,
    )