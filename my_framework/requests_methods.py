from urllib.parse import unquote_plus


class GetRequest:

    @staticmethod
    def parse_input_data(data: str) -> dict:
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_request_params(environ):
        # получаем параметры запроса
        query_string = environ['QUERY_STRING']
        # превращаем параметры в словарь
        request_params = GetRequest.parse_input_data(query_string)
        return request_params


# post requests
class PostRequest:

    @staticmethod
    def get_input_data(environ) -> str:
        content_length_size = int(environ.get('CONTENT_LENGTH', 0))  # получаем длину тела, приводим к int
        print(f'Content_length_size = {content_length_size}')
        # считываем данные, если они есть
        # Тело запроса находится в файле wsgi.input, надо прочитать
        request_body = environ['wsgi.input'].read(content_length_size) if content_length_size > 0 else b''
        # print(type(request_body))
        decoded_body = unquote_plus(request_body.decode('utf-8'))
        # your_name=lala&your_email=bob@gmail.ru&topic=question&your_enquiry=lalala
        print(f'Get dict of byte strings - {decoded_body}')
        return decoded_body

    @staticmethod
    def parse_input_data(data: str) -> dict:
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    def get_request(self, environ):
        # получаем данные
        data = self.get_input_data(environ)
        # превращаем данные в словарь
        new_data = self.parse_input_data(data)
        return new_data
