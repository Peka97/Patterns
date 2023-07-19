Для запуска проекта потребуется ввести следующие команды в терминале:

$ sudo apt-get update
$ sudo apt-get install python3 python3-dev python3-pip

Установить и активировать окружающую среду, затем ввести:
$ pip install wheel
$ pip install uwsgi
$ pip install gunicorn

Запускать из директории lesson_1 с помощью команды:
$ python3 server.py 

Проект доступен по адресу http://127.0.0.1:8000/