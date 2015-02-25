import datetime

from pyzfscore import ZPool, ZFilesystem, ZSnapshot
from dateutil import tz
import mock
from django.test import TestCase
from snapshots.models import Snapshot

from ..util import ZFSHelper


class TestZFSHelper(TestCase):

    @mock.patch('base.util.zfs.ZPool', autospec=ZPool)
    @mock.patch('base.util.zfs.ZFilesystem', autospec=ZFilesystem)
    @mock.patch('base.util.zfs.ZSnapshot', autospec=ZSnapshot)
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
