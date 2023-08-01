from time import time


class Debug:
    def __init__(self, method):
        self.method = method

    def __call__(self, *args, **kwargs):
        start = time()
        result = self.method(args, kwargs)
        timer = time() - start

        print(f'<!> DEBUG | {self.method.__qualname__} - {timer:2.2f} ms <!>')

        return result
