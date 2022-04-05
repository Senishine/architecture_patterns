from jinja2.loaders import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """

    env = Environment()  # создаем объект окружения
    env.loader = FileSystemLoader(folder)  # указываем папку для поиска шаблонов
    template = env.get_template(template_name)  # находим шаблон в окружении
    return template.render(**kwargs)
