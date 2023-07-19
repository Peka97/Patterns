from jinja2 import Template
from os.path import join


def render(template, folder='templates', **kwargs):
    fp = join(folder, template)

    with open(fp, encoding='utf-8') as f:
        template = Template(f.read())

    return template.render(**kwargs)
