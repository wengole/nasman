import datetime

from pyzfscore import ZPool, ZFilesystem, ZSnapshot
from dateutil import tz
import mock
from django.test import TestCase
from snapshots.models import Snapshot

from ..util import ZFSHelper


@mock.patch('base.util.zfs.ZPool', autospec=ZPool)
@mock.patch('base.util.zfs.ZFilesystem', autospec=ZFilesystem)
@mock.patch('base.util.zfs.ZSnapshot', autospec=ZSnapshot)
class TestZFSHelper(TestCase):

    def test_get_snapshots(self, MockZSnapshot, MockZFilesystem, MockZPool):
        zsnap_inst = MockZSnapshot.return_value
        zsnap_inst.name = 'pool@zfs-auto-snap_frequent-2015-01-15-1215'
        zfs_inst = MockZFilesystem.return_value
        zfs_inst.iter_snapshots_sorted.return_value = [zsnap_inst]
        zpool_inst = MockZPool.return_value
        zpool_inst.to_filesystem.return_value = zfs_inst
        MockZPool.list.return_value = [zpool_inst]
        util = ZFSHelper()
        snapshots = util.get_snapshots()
        self.assertEqual(
            snapshots,
            ['pool@zfs-auto-snap_frequent-2015-01-15-1215']
        )

    @mock.patch.object(ZFSHelper, 'get_snapshots')
    def test_create_snapshot_objects(self, mock_get_snaps, *args):
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
    def test_get_all_filesystems(self,
                                 mock_get_pool,
                                 MockZSnapshot,
                                 MockZFilesystem,
                                 MockZPool):
        pool_fs = MockZFilesystem.return_value
        pool_fs.name = 'pool'
        fs1 = mock.MagicMock()
        fs1.name = 'pool/fs1'
        fs2 = mock.MagicMock()
        fs2.name = 'pool/fs2'
        fs3 = mock.MagicMock()
        fs3.name = 'pool/fs2/fs3'
        fs3.iter_filesystems.return_value = []
        fs2.iter_filesystems.return_value = [fs3]
        fs1.iter_filesystems.return_value = []
        pool_fs.iter_filesystems.return_value = [fs1, fs2]
        mock_get_pool.return_value = pool_fs
        util = ZFSHelper()
        filesystems = util.get_all_filesystems()
        self.assertEqual(len(filesystems), 4)
        filesystem_names = [x.name for x in filesystems]
        self.assertIn('pool', filesystem_names)
        self.assertIn('pool/fs1', filesystem_names)
        self.assertIn('pool/fs2', filesystem_names)
        self.assertIn('pool/fs2/fs3', filesystem_names)
