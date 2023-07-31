from datetime import date
from views import *


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/contacts/': Contacts(),
    '/create_category/': CreateCategory(),
    '/categories/': CategoryList(),
    '/create_course/': CreateCourse(),
    '/courses/': CoursesList(),
}
