from framework.responses import *

from framework.requests_ import Get, Post
from framework.decoder import decode_value


class Framework:
    def __init__(self, routes: list, fronts: list):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, env, start_response):
        path = env['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes:
            view = self.routes[path]
        else:
            view = StatusCode404NotFound()

        request = {}

        for front in self.fronts:
            front(request)

        code, body = view(request)
        method = env['REQUEST_METHOD']
        print('method', method)
        if method == 'GET':
            encode_params = Get.parse_input_data(env['QUERY_STRING'])
            request['params'] = decode_value(encode_params)
            print(f"GET | {request['params']}")
        elif method == 'POST':
            encode_data = Post().get_request_params(env)
            request['data'] = decode_value(encode_data)
            print(f"POST | {request['data']}")

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
