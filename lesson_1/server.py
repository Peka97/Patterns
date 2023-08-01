import subprocess

from wsgiref.simple_server import make_server

from framework.main import Framework
from urls import fronts, router


application = Framework(router.routes, fronts)

try:
    with make_server('', 8000, application) as httpd:
        print("Запуск на порту 8000...")
        httpd.serve_forever()

except OSError:
    fuser = subprocess.Popen(
        "fuser -vn tcp 8000",
        shell=True,
        stdout=subprocess.PIPE
    )
    print(fuser.stdout.readlines())
