from framework.responses import *


class Framework:
    def __init__(self, routes: list, fronts: list):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, env, start_response):
        # получаем адрес, по которому выполнен переход
        path = env['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes:
            view = self.routes[path]
        else:
            view = StatusCode404NotFound()
        request = {}
        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
