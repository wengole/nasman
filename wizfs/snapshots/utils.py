from datetime import datetime
import os

from dateutil import parser
from django.utils.timezone import get_default_timezone_name
import pytz
import pyzfscore as zfs

from .models import Snapshot, Filesystem


def root_directory():
    return os.path.abspath(os.path.sep)


class ZFSHelper(object):
    """
    Helper utility for accessing ZFS features
    """
    timezone_name = get_default_timezone_name()

    @staticmethod
    def _get_pool_as_filesystem():
        """
        Get the first available `ZPool` object and return it as a `ZFilesystem`

        :return: The first available pool as a filesystem
        :rtype: `ZFilesystem`
        """
        pools = zfs.ZPool.list()
        if not pools:
            return
        fs = pools[0].to_filesystem()
        return fs

    def get_snapshots(self, fs=None):
        """
        Get a list of snapshot names from the first available pool

        :return: Snapshot names
        :rtype: `list`
        """
        if fs is None:
            fs = self._get_pool_as_filesystem()
        if fs is None:
            return []
        return fs.iter_snapshots_sorted()

    def create_snapshot_objects(self):
        """
        Create `Snapshot` model objects
        """
        snapshots = self.get_snapshots()
        for snap in snapshots:
            creation = datetime.fromtimestamp(
                int(snap.props['creation'].value) * 1000
            )
            try:
                ts_from_name = parser.parse(
                    snap.name,
                    fuzzy=True
                )
            except ValueError:
                ts = creation
            else:
                ts = creation if creation > ts_from_name else ts_from_name
            ts = pytz.timezone(self.timezone_name).localize(ts)
            fs = self.create_filesystem_object(snap.parent)
            snap, created = Snapshot.objects.get_or_create(
                name=snap.name,
                defaults={
                    'timestamp': ts,
                    'filesystem': fs
                }
            )
            if not created:
                snap.timestamp = ts
                snap.filesystem = fs
                snap.save()

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
            if filesystem is None:
                return
        filesystems = [filesystem]
        for f in filesystem.iter_filesystems():
            filesystems.extend(self.get_all_filesystems(f))
        return filesystems

    def create_filesystem_object(self, filesystem):
        """
        Given a `ZFilesystem` object, create a Django `Filesystem` model object

        :param filesystem: filesystem to create object from
        :type filesystem: `ZFilesystem`
        :return: the created Django object
        :rtype: `Filesystem`
        """
        parent = None
        if filesystem.parent_name is not None:
            parentfs = filesystem.parent
            parent = self.create_filesystem_object(parentfs)
        fs, created = Filesystem.objects.get_or_create(
            name=filesystem.name,
        )
        if not created:
            fs.parent = parent
            fs.mountpoint = filesystem.props['mountpoint'].value
            fs.save()
        return fs

    def create_filesystem_objects(self):
        """
        Convenience method to create Django objects for each filesystem
        """
        filesystems = self.get_all_filesystems()
        if filesystems is None:
            return
        for fs in filesystems:
            self.create_filesystem_object(fs)
