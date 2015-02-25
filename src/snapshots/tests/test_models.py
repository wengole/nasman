from django.test import TestCase
from django.utils import timezone
import pytz
from snapshots.models import Snapshot, File


class TestSnapshotModel(TestCase):

    def test_str_method(self):
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


class TestFileModel(TestCase):

    def test_str_method(self):
        file_obj = File.objects.create(
            full_path='/foo/bar',
            created=timezone.now(),
            modified=timezone.now()
        )
        string = str(file_obj)
        unic = unicode(file_obj)
        self.assertIsInstance(string, basestring)
        self.assertIsInstance(unic, unicode)
        self.assertEqual(string, '/foo/bar')
        self.assertEqual(unic, u'/foo/bar')
