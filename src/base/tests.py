from django.core.urlresolvers import resolve
from django.test import TestCase

from .views import HomeView


class TestHomePage(TestCase):
    
    def test_root_url_resolves_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, HomeView.as_view())