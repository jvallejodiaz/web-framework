import unittest
from werkzeug.test import Client
import box
from box.main import app


class TestBase(unittest.TestCase):
    def test_app(self):
        c = Client(app)
        app_iter, status, headers = c.get('/hello_world')

        assert status == '200 OK'

    def test_route(self):

        @app.route('/', endpoint="Index")
        class Index(box.main.EndPoint):
            _name = "Index"

        c = Client(app)
        app_iter, status, headers = c.get('/')

        assert status == '200 OK'


if __name__ == '__main__':
    unittest.main()