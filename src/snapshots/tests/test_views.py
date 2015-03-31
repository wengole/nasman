from celery import states
from django.core.cache import cache
from django.test import TestCase, Client
from snapshots.models import Filesystem
from snapshots.views import get_status_dict


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

    def tests_get_status_dict(self):
        fs = Filesystem.objects.create(
            name=u'test_status'
        )
        status = get_status_dict(fs)
        self.assertEqual(
            status,
            {'state': 'NOTFOUND',
             'progress': 0.0,
             'total': 0,
             'done': 0}
        )

        fs.reindex_status = MockAsyncResult(states.FAILURE)
        status = get_status_dict(fs)
        self.assertEqual(status['state'], states.FAILURE)

        fs.reindex_status = MockAsyncResult(states.STARTED, 10, 100, 10)
        status = get_status_dict(fs)
        self.assertEqual(status['state'], states.STARTED)
        self.assertEqual(status['progress'], 10)
        self.assertEqual(status['total'], 100)
        self.assertEqual(status['done'], 10)

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
