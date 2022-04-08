from time import time


class AppRoute:
    """Декоратор для добавления связки url-view в приложение"""

    def __init__(self, routes, url):
        '''Сохраняем значение переданного параметра'''
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    """Декоратор для отображения в терминале название функции и время ее выполнения"""

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        # эта вспомогательная функция будет декорировать каждый отдельный метод класса
        def timeit(method):
            '''
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            '''

            def timed(*args, **kw):
                before = time()
                result = method(*args, **kw)
                after = time()
                delta = after - before

                print(f'Выполнился метод {self.name} за {delta:2.2f} мс')
                return result

            return timed

        return timeit(cls)
