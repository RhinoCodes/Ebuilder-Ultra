# api.py
from webob import Request, Response
import re

class ultra:
    def __init__(self):
        self.routes = {}
    
    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def parse(self, a, b):
        args = re.compile("<(\w+)>")
        base = a[0:a.find("<")]
        if b.startswith(base) and b != base:
            return b[b.find(base)+len(base):]

    def find(self, stra, strb):
        return_value = stra.find(strb)
        if return_value == -1:
            return_value = len(stra)-1

        return return_value

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            if request_path.startswith(path[0:self.find(path, "<")]):
                parse_result = self.parse(path, request_path)
                if parse_result is not None:
                    return handler(parse_result)
                else:
                    return handler()

        return None

    def handle_request(self, request):
        response = Response()

        handler = self.find_handler(request.path)
        if handler is not None:
            response.text = handler
            return response
            
        self.page_not_found(response)
        return response

    def page_not_found(self, response):
        response.status_code = 404
        response.text = "<h1 style='text-align: center'>404 Page Not Found</h1>"
        
    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper
