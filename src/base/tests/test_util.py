from pyzfscore import ZPool, ZFilesystem, ZSnapshot
from mock import patch
from django.test import TestCase

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