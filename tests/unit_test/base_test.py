import unittest
from werkzeug.wrappers import Response
from werkzeug.test import Client, EnvironBuilder
import box
from box.main import app, Request


class TestBase(unittest.TestCase):

    def test_app(self):
        c = Client(app)
        app_iter, status, headers = c.get('/hello_world')

        assert status == '200 OK'

    def test_dispatch(self):
        builder = EnvironBuilder(path='/hello_world', method='GET')
        env = builder.get_environ()
        request = Request(env)
        response = app.dispatch_request(request)

        assert isinstance(response, Response)

    def test_route(self):

        @app.route('/', endpoint="Index")
        class Index(box.main.EndPoint):
            _name = "Index"

        c = Client(app)
        app_iter, status, headers = c.get('/')

        assert status == '200 OK'


if __name__ == '__main__':
    unittest.main()