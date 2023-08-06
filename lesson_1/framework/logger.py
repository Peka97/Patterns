class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class ConsoleWriter:
    def write(self, message):
        print(message)


class FileWriter:
    def __init__(self, fp: str):
        self.fp = 'path'

    def write(self, message):
        with open(self.fp, 'a', encoding='utf-8') as f:
            f.write(f'{message}\n')


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, message):
        self.writer.write(message)
