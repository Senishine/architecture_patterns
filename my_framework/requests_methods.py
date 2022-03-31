# -*- coding: utf-8 -*-

from urllib.parse import unquote_plus


def parse_data(data: str):
    """ Функция разделяет строку с параметрами запроса по парам по '&' и '=',
    складывая ключи и значения в словарь"""
    result = {}
    if data:
        params = data.split('&')  # делим на пары
        for item in params:
            key, value = item.split('=')
            result[key] = value
    return result


class GetRequest:

    @staticmethod
    def get_request_str(environ) -> dict:
        return parse_data(unquote_plus(environ['QUERY_STRING'], encoding='utf-8'))


class PostRequest:

    @staticmethod
    def get_body(env) -> bytes:
        content_size = env.get('CONTENT_LENGTH')  # сначала надо проверить наличие длины данных (тела запроса)
        content_length = int(content_size) if content_size else 0
        print(content_length)
        # тело запроса содержится в env['wsgi.input'] <class '_io.BufferedReader'>, читаем данные (байты)
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_body_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = unquote_plus(data.decode(), encoding='utf-8')  # т.к. данные пришли в байтах, декодируем данные
            print(f'строка после декод - {data_str}')
            result = parse_data(data_str)
        return result

    def get_request_body(self, environ):
        data = self.get_body(environ)  # получаем данные
        return self.parse_body_data(data)  # превращаем данные в словарь
