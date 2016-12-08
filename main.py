import os
import werkzeug
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.routing import Map, Rule


class App(object):

    def __init__(self):
        self.url_map = Map()
        self.rule = Rule

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return globals()[endpoint](request, **values)
        except HTTPException, e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def route(self, route, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            rule = self.rule(route, endpoint=f.func_name,**options)
            self.url_map.add(rule)
            return f
        return decorator
app = App()

@app.route('/hello_world', endpoint='hello_world')
def hello_world(self):
    return Response('Hello World')

def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)