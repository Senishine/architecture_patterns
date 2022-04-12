from copy import deepcopy
from quopri import decodestring
from patterns.behavioral_patterns import Subject, FileWriter


class User:
    """ Абстрактный класс пользователя"""

    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, user_type, name):
        """ Паттерн Фабричный метод"""
        return cls.types[user_type](name)


class CoursePrototype:
    """Паттерн Прототип - создает копию объекта"""

    def copy(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


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
    def create_user(user_type, name):
        return UserFactory.create(user_type, name)

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

    def __init__(self, name, writer):
        self.name = name
        self.writer = writer

    def log(self, text):
        print('Log:', text)
        self.writer.write(text)
