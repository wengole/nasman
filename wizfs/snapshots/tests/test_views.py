from django.core.cache import cache
from django.test import TestCase, Client


class MockAsyncResult(object):
    state = None
    info = None

    def __init__(self, state, progress=0, total=0, done=0):
        self.state = state
        self.info = {
            'percentage': progress,
            'total': total,
            'done': done
        }


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        cache.delete_pattern(u'reindex_*')

    def tearDown(self):
        cache.delete_pattern(u'reindex_*')

    def test_dashboard_view(self):
        response = self.client.get('/')
        expected =u'WiZFS Dashboard'
        self.assertIn(expected, response.content.decode())

    def test_filesystemlist_ajax(self):
        response = self.client.get(
            '/filesystems',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        pass
