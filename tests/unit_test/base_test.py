import unittest
from werkzeug.wrappers import Response
from werkzeug.test import Client, EnvironBuilder
import box
from box.main import app, Request


class TestBase(unittest.TestCase):

    def setUp(self):
        @app.route('/', endpoint="Index")
        class Index(box.main.EndPoint):
            _name = "Index"

    def test_app(self):
        c = Client(app)
        app_iter, status, headers = c.get('/')

        assert status == '200 OK'

    def test_dispatch(self):
        builder = EnvironBuilder(path='/', method='GET')
        env = builder.get_environ()
        request = Request(env)
        response = app.dispatch_request(request)

        assert isinstance(response, Response)

    def test_route(self):

        @app.route('/test_route', endpoint='TestRoute')
        class TestRoute(box.main.EndPoint):
            _name = "TestRoute"

        c = Client(app)
        app_iter, status, headers = c.get('/test_route')

        assert status == '200 OK'

    def test_endpoint_inheritance(self):

        @app.route('/hello_world', endpoint='HelloWorld')
        class HelloWorld(box.main.EndPoint):
            _name = "HelloWorld"

            @classmethod
            def check_inheritance(name=None):
                return "Hello World"

            @classmethod
            def dispatch_request(name=None):
                return "Hello World"

        @app.route('/hello_world', endpoint='HelloWorld')
        class HelloWorld2(HelloWorld):
            _name = "HelloWorld2"

            @classmethod
            def dispatch_request(name=None):
                return "Hello World 2"

        assert HelloWorld.dispatch_request() == "Hello World"
        assert HelloWorld2.dispatch_request() == "Hello World 2"
        assert HelloWorld.check_inheritance() == HelloWorld2.check_inheritance()

    def test_data(self):
        @app.route('/test_data', endpoint='TestData')
        class TestData(box.main.EndPoint):
            _name = "TestData"

            @classmethod
            def dispatch_request(name=None):
                return Response("TestData")

        builder = EnvironBuilder(path='/test_data', method='GET')
        env = builder.get_environ()
        request = Request(env)
        response = app.dispatch_request(request)

        assert response.data == "TestData"

    def test_json(self):
        @app.route('/json_request', endpoint='JsonRequest', methods=['POST'])
        class JsonRequest(box.main.EndPoint):
            _name = "JsonRequest"

        c = Client(app)
        app_iter, status, headers = c.post('/json_request', content_type="application/json")

        assert status == '200 OK'




if __name__ == '__main__':
    unittest.main()