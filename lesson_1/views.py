from datetime import date

from framework.templator import render
from patterns import Engine, Logger
from routes import Router
from debug import Debug

site = Engine()
logger = Logger('main')
router = Router
debug = Debug


@router(url='/')
class Index:
    @Debug
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


@router(url='/contacts/')
class Contacts:
    @Debug
    def __call__(self, request):
        return '200 OK', render('contacts.html')


@router(url='/categories/')
class CategoryList:
    @Debug
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('categories.html',
                                objects_list=site.categories)


@router(url='/courses/')
class CoursesList:
    @Debug
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('courses.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id
                                    )
        except KeyError:
            return '200 OK', render('courses.html',
                                    error='<!> Нет ни одной категории. Отображение курсов невозможно <!>'
                                    )


@router(url='/create_category/')
class CreateCategory:
    def __call__(self, request):
        if request.get('method') == 'POST':
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
            return '200 OK', render('create_category.html',
                                    categories=categories)


@router(url='/create_course/')
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request.get('method') == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('courses.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', render('create_course.html',
                                        error='<!> Нет ни одной категории. Создание курса невозможно <!>'
                                        )


class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)
        except KeyError:
            return '200 OK', render('course_list.html',
                                    error='<!> Нет ни одной категории. Создание курса невозможно <!>'
                                    )
