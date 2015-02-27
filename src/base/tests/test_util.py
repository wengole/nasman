import datetime

from pyzfscore import ZPool, ZFilesystem, ZSnapshot
from dateutil import tz
import mock
from django.test import TestCase
from snapshots.models import Snapshot, Filesystem

from ..util import ZFSHelper


class TestZFSHelper(TestCase):

    def setUp(self):
        self.snap = mock.MagicMock()
        self.snap.name = 'pool@zfs-auto-snap_frequent-2015-01-15-1215'
        self.pool_fs = mock.MagicMock()
        self.pool_fs.name = 'pool'
        self.pool_fs.iter_snapshots_sorted.return_value = [self.snap]
        self.pool = mock.MagicMock()
        self.pool.to_filesystem.return_value = self.pool_fs
        self.fs1 = mock.MagicMock()
        self.fs1.name = 'pool/fs1'
        self.fs2 = mock.MagicMock()
        self.fs2.name = 'pool/fs2'
        self.fs3 = mock.MagicMock()
        self.fs3.name = 'pool/fs2/fs3'
        self.fs3.iter_filesystems.return_value = []
        self.fs2.iter_filesystems.return_value = [self.fs3]
        self.fs1.iter_filesystems.return_value = []
        self.pool_fs.iter_filesystems.return_value = [self.fs1, self.fs2]

    @mock.patch('base.util.zfs.ZPool')
    def test_get_snapshots(self, MockZPool):
        MockZPool.list.return_value = [self.pool]
        util = ZFSHelper()
        snapshots = util.get_snapshots()
        self.assertEqual(
            snapshots,
            ['pool@zfs-auto-snap_frequent-2015-01-15-1215']
        )

    @mock.patch.object(ZFSHelper, 'get_snapshots')
    def test_create_snapshot_objects(self, mock_get_snaps):
        fake_snaps = [
            'pool@snap1',
            'pool@zfs-auto-snap_frequent-2015-01-15-1215',
            'pool@2015-02-15-0915',
            'pool@2015-13-99-0915',
        ]
        mock_get_snaps.return_value = fake_snaps
        util = ZFSHelper()
        util.create_snapshot_objects()
        self.assertEqual(Snapshot.objects.all().count(), len(fake_snaps))
        snap1 = Snapshot.objects.get(
            name='pool@zfs-auto-snap_frequent-2015-01-15-1215'
        )
        self.assertEqual(
            snap1.timestamp,
            datetime.datetime(2015, 1, 15, 12, 15, tzinfo=tz.tzutc())
        )
        snap2 = Snapshot.objects.get(
            name='pool@2015-02-15-0915'
        )
        self.assertEqual(
            snap2.timestamp,
            datetime.datetime(2015, 2, 15, 9, 15, tzinfo=tz.tzutc())
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
        fs2 = Filesystem.objects.get(
            name='pool/fs2'
        )
        self.assertEqual(fs2.parent, pool_fs)
        fs3 = Filesystem.objects.get(
            name='pool/fs2/fs3'
        )
        self.assertEqual(fs3.parent, fs2)
