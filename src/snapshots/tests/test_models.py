import shutil
import os

from django.test import TestCase
from django.utils import timezone
from snapshots.models import Snapshot, File, Filesystem


class TestSnapshotModel(TestCase):

    def setUp(self):
        self.test_pool = u'test-pool'
        self.test_fs = Filesystem.objects.create(
            name=self.test_pool,
            mountpoint=self.test_pool
        )

    def tearDown(self):
        if os.path.exists(self.test_pool):
            shutil.rmtree(self.test_pool)

    def test_str_method(self):
        snapshot = Snapshot.objects.create(
            name=u'a test',
            filesystem=self.test_fs
        )
        string = str(snapshot)
        unic = unicode(snapshot)
        self.assertIsInstance(string, basestring)
        self.assertIsInstance(unic, unicode)
        self.assertEqual(string, b'a test')
        self.assertEqual(unic, u'a test')

    def test_name_methods(self):
        snapshot = Snapshot.objects.create(
            name=u'%s@foo-bar' % self.test_pool,
            filesystem=self.test_fs
        )
        self.assertEqual(snapshot.base_name, u'foo-bar')
        self.assertEqual(snapshot.parent_name, self.test_pool)

    def test_walk_snapshot(self):
        snapshot = Snapshot.objects.create(
            name=u'%s@foo-bar' % self.test_pool,
            filesystem=self.test_fs
        )
        os.makedirs(u'%s/.zfs/snapshot/foo-bar/test-dir' % self.test_pool)
        x = snapshot.walk_snapshot()
        dirname, subdirs, filenames = next(x)
        self.assertIn(u'test-dir', subdirs)


class TestFileModel(TestCase):

    def test_str_method(self):
        file_obj = File.objects.create(
            full_path=u'/foo/bar',
            created=timezone.now(),
            modified=timezone.now()
        )
        string = str(file_obj)
        unic = unicode(file_obj)
        self.assertIsInstance(string, basestring)
        self.assertIsInstance(unic, unicode)
        self.assertEqual(string, b'/foo/bar')
        self.assertEqual(unic, u'/foo/bar')
