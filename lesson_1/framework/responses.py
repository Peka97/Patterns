class StatusCode200OK:
    def __call__(self, request):
        return '200 OK', '200 OK'


class StatusCode401Unauthorized:
    def __call__(self, request):
        return '401 Unauthorized', '401 Unauthorized'


class StatusCode403Forbidden:
    def __call__(self, request):
        return '403 Forbidden', '403 Forbidden'


class StatusCode404NotFound:
    def __call__(self, request):
        return '404 NotFound', '404 NotFound'


class StatusCode500InternalServerError:
    def __call__(self, request):
        return '500 Internal Server Error', '500 Internal Server Error'
