from django.test import TestCase
from snapshots.models import Snapshot


class TestSnapshotModel(TestCase):

    def test_unicode_method(self):
        snapshot = Snapshot.objects.create(
            name='a test',
            timestamp=None
        )
        string = str(snapshot)
        unic = unicode(snapshot)
        self.assertIsInstance(string, basestring)
        self.assertIsInstance(unic, unicode)
        self.assertEqual(string, 'a test')
        self.assertEqual(unic, u'a test')
