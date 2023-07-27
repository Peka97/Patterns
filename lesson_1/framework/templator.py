from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template
from os.path import join


# def render(template, folder='templates', **kwargs):
#     fp = join(folder, template)

#     with open(fp, encoding='utf-8') as f:
#         template = Template(f.read())

#     return template.render(**kwargs)


def render(template_name, folder='templates', **kwargs):
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)
