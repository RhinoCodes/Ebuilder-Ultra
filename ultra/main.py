# api.py
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from webob import Request, Response
from functools import lru_cache
import re, inspect


class DuplicateRoute(Exception):
    pass

class request_class:
    def __init__(self):
        self.method = 'GET'
        self.url = '/'
        self.data = {}
        pass

    def __setMethod__(self, method):
        self.method = method

    def __setData__(self, data):
        self.data = data

    def __setUrl__(self, url):
        self.url = url

request = request_class()

class Ultra:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def test_session(self, base_url="http://localhost:8000"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    @lru_cache(maxsize=100, typed=False)
    def parse(self, stra, strb):
        if stra.__contains__("<"):
            x = re.compile("<(\w+)>")
            b = x.search(stra).groups()

            return_value = {}
            for i in b:
                z = stra.replace("<" + i + ">", "(\w+)")
                return_value[i] = re.compile(z).search(strb).groups()[0]

            return return_value

        return None

    def find(self, stra, strb):
        return_value = stra.find(strb)
        if return_value == -1:
            return_value = len(stra) +1

        return return_value

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = self.parse(path, request_path)
            if parse_result is not None:
                if parse_result is not None:
                    return handler, parse_result
            elif path == request_path:
                return handler, {}

        return None, None

    def handle_request(self, request):
        response = Response()
        globals()["request"].__setMethod__(request.method)
        globals()["request"].__setData__(request.params)
        globals()["request"].__setUrl__(request.url)
        import json
        
        handler, kwargs = self.find_handler(request.path)
        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is not None:
                    response.text = handler(**kwargs)
                else:
                    self.method_not_allowed(response, request.method)
            
            elif isinstance(handler, str):
                response.text = handler(**kwargs)
            elif isinstance(handler, dict):
                response.json = handler(**kwargs)

            else:
                response.text = str(handler(**kwargs))

            return response

        self.page_not_found(response)
        return response

    def page_not_found(self, response):
        response.status_code = 404
        response.text = """<h1 style="text-align: center; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;">404 Page Not Found</h1>"""

    def method_not_allowed(self, response, method):
        response.status_code = 405
        response.text = f"""<h1 style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;">No Handler for {method}</h1><p style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;">You are seeing this because this method has been blocked or, the creator did not specify a way to deal with it.</p>"""

    def route(self, path):
        def wrapper(handler):
            if path not in self.routes.keys():
                self.routes[path] = handler
                return handler
            else:
                raise DuplicateRoute(f"The route {path} already exists")

        return wrapper

    def restart(self):
        self.server.server_close()
        self.server.serve_forever()

    def run(self, port=8000, debug=False):
        from wsgiref.util import setup_testing_defaults
        from wsgiref.simple_server import make_server

        self.server = make_server("", port, self)
        with self.server as httpd:
            print(f"Serving on port {port}\nDebug Server - Don't use in production!")
            httpd.serve_forever()
