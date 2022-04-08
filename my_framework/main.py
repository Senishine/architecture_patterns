# -*- coding: utf-8 -*-
from my_framework.requests_methods import GetRequest, PostRequest


class Framework:
    """Base framework's class"""

    def __init__(self, routes, fronts_funcs):
        self.routes_lst = routes
        self.fronts_lst = fronts_funcs

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']  # get requested url

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            request['data'] = PostRequest().get_request_body(environ)
            print(f'Нам пришёл post-запрос: {request["data"]}')

        if method == 'GET':
            request['request_params'] = GetRequest().get_request_str(environ)
            print(f'Нам пришли GET-параметры: {request["request_params"]}')

        if path in self.routes_lst:  # apply page controller pattern
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        for front in self.fronts_lst:  # apply front controller pattern, fill request from front_funcs
            front(request)

        code, body = view(request)  # call the view with request object
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


class PageNotFound404:
    def __call__(self, request):
        return '404 Error', 'Page not found, return to <a href="/">main</a> page.'


class DebugInfo(Framework):
    """WSGI-application —  для каждого запроса выводит информацию (тип запроса и параметры) в консоль"""

    def __init__(self, routes, fronts_funcs):
        self.application = Framework(routes, fronts_funcs)
        super().__init__(routes, fronts_funcs)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


class FakeApp(Framework):
    """WSGI-application фейковый (на все запросы пользователя отвечает “200 OK”, “Hello from Fake”)"""

    def __init__(self, routes, fronts_funcs):
        self.application = Framework(routes, fronts_funcs)
        super().__init__(routes, fronts_funcs)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return b'Hello from Fake'
