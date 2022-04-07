from my_framework.rendering import render
from patterns import creational_patterns

site = creational_patterns.Engine()


class HomePage:
    def __call__(self, request):
        return '200 OK', render('index.html')


class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html')


class CreateCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


class CategoryList:
    def __call__(self, request):
        return '200 OK', render('category_list.html', objects_list=site.categories)


class CreateCourse:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = site.find_category_by_id(int(self.category_id))
            course = site.create_course('business', name, category)
            site.courses.append(course)

            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


class CoursesList:
    def __call__(self, request):
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            current_course = site.get_course(name)
            if current_course:
                new_name = f'copy_{name}'
                new_course_name = current_course.copy()
                new_course_name.name = new_name
                site.courses.append(new_course_name)

            return '200 OK', render('course_list.html', objects_list=site.courses, name=new_course_name.category.name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
