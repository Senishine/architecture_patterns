from datetime import date
from views import HomePage, About, Contact, CreateCategory, CategoryList, CreateCourse, CoursesList, CopyCourse


# front controller
def time_front(request):
    request['date'] = date.today()


def secret_key_front(request):
    request['key'] = 'key'


fronts = [time_front, secret_key_front]

routes = {
    '/': HomePage(),
    '/about/': About(),
    '/contact/': Contact(),
    '/create_category/': CreateCategory(),
    '/category_list/': CategoryList(),
    '/create_course/': CreateCourse(),
    '/courses_list/': CoursesList(),
    '/copy_course/': CopyCourse()
}
