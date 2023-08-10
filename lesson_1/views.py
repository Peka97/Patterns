from datetime import date

from framework.templator import render

from objects import Engine, MapperRegistry
from framework.logger import Logger
from framework.notifier import EmailNotifier, SmsNotifier
from framework.views import ListView, CreateView
from framework.unitofwork import UnitOfWork
from routes import Router
from debug import Debug


site = Engine()
logger = Logger('main')
router = Router
debug = Debug
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@router('/')
class Index:
    @Debug
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


@router('/contacts/')
class Contacts:
    @Debug
    def __call__(self, request):
        return '200 OK', render('contacts.html')


@router('/categories/')
class CategoryList:
    @Debug
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('categories.html',
                                objects_list=site.categories)


@router('/courses/')
class CoursesList:
    @Debug
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            # category = site.find_category_by_id(
            #     int(request['request_params']['id']))
            return '200 OK', render('courses.html',
                                    objects_list=site.courses,
                                    name=site.categories[0].name)
        except KeyError:
            return '200 OK', render('courses.html',
                                    error='<!> Нет ни одной категории. Отображение курсов невозможно <!>'
                                    )


@router('/create_category/')
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


@router('/create_course/')
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


@router('/students/')
class StudentListView(ListView):
    template_name = 'students.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@router('/create_student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@router('/add_student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)
