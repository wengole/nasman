from django.test import TestCase, Client


class BaseTestCase(TestCase):
    """
    Our Base Test Case to contain handy helper methods
    """
    def setUp(self):
        self.client = Client()

    # TODO: For reference. This might be useful later
    # def setup_view(view, request, *args, **kwargs):
    #     """Mimic as_view() returned callable, but returns view instance.
    #
    #     args and kwargs are the same you would pass to ``reverse()``
    #
    #     """
    #     view.request = request
    #     view.args = args
    #     view.kwargs = kwargs
    #     return view

