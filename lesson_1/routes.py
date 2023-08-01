class Router:
    routes = {}

    def __init__(self, url):
        self.url = url

    def __call__(self, cls):
        self.__class__.routes[self.url] = cls()
