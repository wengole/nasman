from django.test import TestCase, RequestFactory
from wizfs.wsgi import application


class TestWSGI(TestCase):

    def test_get_wsgi_application(self):
        """
        Verify that ``get_wsgi_application`` returns a functioning WSGI
        callable.
        """
        environ = RequestFactory()._base_environ(
            PATH_INFO="/",
            CONTENT_TYPE="text/html; charset=utf-8",
            REQUEST_METHOD="GET"
        )

        response_data = {}

        def start_response(status, headers):
            response_data["status"] = status
            response_data["headers"] = headers

        response = application(environ, start_response)

        self.assertEqual(response_data["status"], "200 OK")
        self.assertEqual(
            response_data["headers"],
            [('X-Frame-Options', 'SAMEORIGIN'),
             ('Content-Type', 'text/html; charset=utf-8')])
        self.assertIn(
            b"WiZFS",
            bytes(response)
            )