from copy import deepcopy
from quopri import decodestring


class User:
    """ Абстрактный класс пользователя"""
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, user_type):
        """ Паттерн Фабричный метод"""
        return UserFactory.types[user_type]()


class CoursePrototype:
    """Паттерн Прототип - создает копию объекта"""

    def copy(self):
        return deepcopy(self)


class Course(CoursePrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class BusinessEnglish(Course):
    pass


class GeneralEnglish(Course):
    pass


class CourseFactory:
    types = {
        'business': BusinessEnglish,
        'general': GeneralEnglish
    }

    @classmethod
    def create(cls, course_type, name, category):
        return CourseFactory.types[course_type](name, category)


class Category:
    id_counter = 0

    def __init__(self, name, category):
        self.id = Category.id_counter
        Category.id_counter += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(user_type):
        return UserFactory.create(user_type)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, cat_id):
        for item in self.categories:
            print('item', item.id)
            if item.id == cat_id:
                return item
        raise Exception(f'Нет категории с id = {cat_id}')

    @staticmethod
    def create_course(course_type, name, category):
        return CourseFactory.create(course_type, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        name = ''
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name not in cls.__instance:
            cls.__instance[name] = super().__call__(*args, **kwargs)
        return cls.__instance[name]


class Logger(metaclass=Singleton):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('Log:', text)
