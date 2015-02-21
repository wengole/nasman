from django.template.loader import render_to_string

from .base import BaseTestCase


class TestHomeView(BaseTestCase):

    def test_root_url_renders_correct_template(self):
        response = self.client.get('/')
        expected = 'Dashboard sub section'
        self.assertIn(expected, response.content.decode())
