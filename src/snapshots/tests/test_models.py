import shutil
import os

from django.test import TestCase
from django.utils import timezone
from snapshots.models import Snapshot, File

test_pool = 'test-pool'


class TestSnapshotModel(TestCase):

    def tearDown(self):
        if os.path.exists(test_pool):
            shutil.rmtree(test_pool)

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

    def test_name_methods(self):
        snapshot = Snapshot.objects.create(
            name='%s@foo-bar' % test_pool
        )
        self.assertEqual(snapshot.base_name, 'foo-bar')
        self.assertEqual(snapshot.parent_name, test_pool)

    def test_walk_snapshot(self):
        snapshot = Snapshot.objects.create(
            name='%s@foo-bar' % test_pool
        )
        os.makedirs('%s/.zfs/snapshot/foo-bar/test-dir' % test_pool)
        x = snapshot.walk_snapshot()
        dirname, subdirs, filenames = next(x)
        self.assertIn(u'test-dir', subdirs)


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
