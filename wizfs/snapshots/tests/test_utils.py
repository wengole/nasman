import datetime

from dateutil import tz
from django.test import TestCase
import mock

from ..models import Snapshot, Filesystem
from ..utils import ZFSHelper


class TestZFSHelper(TestCase):

    def setUp(self):
        self.snap1 = mock.MagicMock()
        self.snap1.name = 'pool@zfs-auto-snap_frequent-2015-01-15-1215'
        self.snap2 = mock.MagicMock()
        self.snap2.name = 'pool/fs1@snap2'
        self.snap3 = mock.MagicMock()
        self.snap3.name = 'pool/fs2/fs3@2015-02-15-0915'
        self.snap4 = mock.MagicMock()
        self.snap4.name = 'pool@2015-13-99-0915'
        self.pool_fs = mock.MagicMock()
        self.snap1.parent = self.pool_fs
        self.snap4.parent = self.pool_fs
        self.pool_fs.name = 'pool'
        self.pool_fs.parent_name = None
        self.pool_fs.parent = None
        self.pool_fs.is_mounted.return_value = '/pool'
        self.pool_fs.iter_snapshots_sorted.return_value = [
            self.snap1,
            self.snap4
        ]
        self.pool = mock.MagicMock()
        self.pool.to_filesystem.return_value = self.pool_fs
        self.fs1 = mock.MagicMock()
        self.fs1.name = 'pool/fs1'
        self.fs1.parent_name = 'pool'
        self.fs1.parent = self.pool_fs
        self.fs1.is_mounted.return_value = '/pool/fs1'
        self.snap2.parent = self.fs1
        self.fs2 = mock.MagicMock()
        self.fs2.name = 'pool/fs2'
        self.fs2.is_mounted.return_value = '/pool/fs2'
        self.fs2.parent_name = 'pool'
        self.fs2.parent = self.pool_fs
        self.fs3 = mock.MagicMock()
        self.fs3.name = 'pool/fs2/fs3'
        self.fs3.is_mounted.return_value = '/pool/fs2/fs3'
        self.fs3.parent_name = 'pool/fs2'
        self.fs3.parent = self.fs2
        self.fs3.iter_filesystems.return_value = []
        self.snap3.parent = self.fs3
        self.fs2.iter_filesystems.return_value = [self.fs3]
        self.fs1.iter_filesystems.return_value = []
        self.pool_fs.iter_filesystems.return_value = [self.fs1, self.fs2]

    @mock.patch('snapshots.utils.zfs.ZPool')
    def test_get_snapshots(self, MockZPool):
        MockZPool.list.return_value = [self.pool]
        util = ZFSHelper()
        snapshots = util.get_snapshots()
        snapshots = [x.name for x in snapshots]
        self.assertEqual(
            snapshots,
            ['pool@zfs-auto-snap_frequent-2015-01-15-1215',
             'pool@2015-13-99-0915']
        )

    @mock.patch('snapshots.utils.zfs.ZPool')
    def test_create_snapshot_objects(self, MockZPool):
        MockZPool.list.return_value = [self.pool]
        util = ZFSHelper()
        util.create_snapshot_objects()
        self.assertEqual(Snapshot.objects.all().count(), 2)
        snap1 = Snapshot.objects.get(
            name=u'pool@zfs-auto-snap_frequent-2015-01-15-1215'
        )
        self.assertEqual(
            snap1.timestamp,
            datetime.datetime(2015, 1, 15, 12, 15, tzinfo=tz.tzutc())
        )
        snap2 = Snapshot.objects.get(
            name=u'pool@2015-13-99-0915'
        )
        self.assertIsNone(
            snap2.timestamp
        )

    @mock.patch.object(ZFSHelper, '_get_pool_as_filesystem')
    def test_get_all_filesystems(self, mock_get_pool):
        mock_get_pool.return_value = self.pool_fs

        util = ZFSHelper()
        filesystems = util.get_all_filesystems()
        self.assertEqual(len(filesystems), 4)
        filesystem_names = [x.name for x in filesystems]
        self.assertIn('pool', filesystem_names)
        self.assertIn('pool/fs1', filesystem_names)
        self.assertIn('pool/fs2', filesystem_names)
        self.assertIn('pool/fs2/fs3', filesystem_names)

    @mock.patch.object(ZFSHelper, 'get_all_filesystems')
    def test_create_filesystem_objects(self, mock_get_fs):
        mock_get_fs.return_value = [self.pool_fs, self.fs1, self.fs2, self.fs3]

        util = ZFSHelper()
        util.create_filesystem_objects()
        pool_fs = Filesystem.objects.get(
            name='pool',
        )
        self.assertIsNone(pool_fs.parent)
        self.assertEqual(pool_fs.mountpoint, '/pool')
        fs2 = Filesystem.objects.get(
            name='pool/fs2'
        )
        self.assertEqual(fs2.parent, pool_fs)
        self.assertEqual(fs2.mountpoint, '/pool/fs2')
        fs3 = Filesystem.objects.get(
            name='pool/fs2/fs3'
        )
        self.assertEqual(fs3.mountpoint, '/pool/fs2/fs3')
        self.assertEqual(fs3.parent, fs2)
