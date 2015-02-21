from django.test import TestCase, RequestFactory

from menu import Menu


class TestMenus(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_menu_on_dashboard(self):
        request = self.factory.get('/')
        Menu.process(request, 'top_nav_left')
        mitems = Menu.items['top_nav_left']
        self.assertEqual(len(mitems), 1)
        self.assertEqual(len(mitems[0].children), 2)
        self.assertFalse(mitems[0].selected)
