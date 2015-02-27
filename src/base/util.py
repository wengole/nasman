from django.utils.timezone import get_default_timezone_name
import pytz
import pyzfscore as zfs
from dateutil import parser
from snapshots.models import Snapshot, Filesystem


class ZFSHelper(object):
    """
    Helper utility for accessing ZFS features
    """
    timezone_name = get_default_timezone_name()

    def _get_pool_as_filesystem(self):
        """
        Get the first available `ZPool` object and return it as a `ZFilesystem`

        :return: The first available pool as a filesystem
        :rtype: `ZFilesystem`
        """
        pool = zfs.ZPool.list()[0]
        fs = pool.to_filesystem()
        return fs

    def get_snapshots(self):
        """
        Get a list of snapshot names from the first available pool

        :return: Snapshot names
        :rtype: `list`
        """
        fs = self._get_pool_as_filesystem()
        snapshots = fs.iter_snapshots_sorted()
        return [x.name for x in snapshots]

    def create_snapshot_objects(self):
        """
        Create `Snapshot` model objects
        """
        snapshots = self.get_snapshots()
        for snap in snapshots:
            try:
                ts = parser.parse(snap, fuzzy=True)
                pytz.timezone(self.timezone_name).localize(ts)
            except ValueError:
                ts = None
            Snapshot.objects.get_or_create(
                name=snap,
                timestamp=ts
            )

    def get_all_filesystems(self, filesystem=None):
        """
        Recursively get all filesystems in the ZFS hierarchy

        :param filesystem: starting filesystem, if `None` then start from pool
        :type filesystem: `ZFilesystem`
        :return: a list of all filesystems
        :rtype: `list`
        """
        if filesystem is None:
            filesystem = self._get_pool_as_filesystem()
        filesystems = [filesystem]
        for f in filesystem.iter_filesystems():
            filesystems.extend(self.get_all_filesystems(f))
        return filesystems

    def create_filesystem_object(self, fs_name):
        """
        Given a `ZFilesystem` object, create a Django `Filesystem` model object

        :param filesystem: filesystem to create object from
        :type filesystem: `ZFilesystem`
        :return: the created Django object
        :rtype: `Filesystem`
        """
        parent = None
        parent_name = '/'.join(fs_name.split('/')[:-1])
        if parent_name != '':
            parent = self.create_filesystem_object(parent_name)
        fs, _ = Filesystem.objects.get_or_create(
            name=fs_name,
            parent=parent,
        )
        return fs

    def create_filesystem_objects(self):
        """
        Convenience method to create Django objects for each filesystem
        """
        filesystems = self.get_all_filesystems()
        for fs in filesystems:
            self.create_filesystem_object(fs.name)
