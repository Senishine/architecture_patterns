class Framework:
    """Base framework's class"""

    def __init__(self, routes, fronts_funcs):
        self.routes_lst = routes
        self.fronts_lst = fronts_funcs

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']  # get requested url

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes_lst:  # apply page controller pattern
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()
        request = {}

        for front in self.fronts_lst:  # apply front controller pattern, fill request from front_funcs
            front(request)

        code, body = view(request)  # call the view with request object
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


class PageNotFound404:
    def __call__(self, request):
        return '404 Error', 'Page not found, return to <a href="/">main</a> page.'
