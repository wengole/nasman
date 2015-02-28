from datetime import datetime
import magic
import os
from django.utils.timezone import get_default_timezone_name
import pytz
import pyzfscore as zfs
from dateutil import parser

from .models import Snapshot, Filesystem, File


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
        return [{'name': x.name,
                'parent': x.parent} for x in snapshots]

    def create_snapshot_objects(self):
        """
        Create `Snapshot` model objects
        """
        snapshots = self.get_snapshots()
        for snap in snapshots:
            try:
                ts = parser.parse(snap['name'], fuzzy=True)
                ts = pytz.timezone(self.timezone_name).localize(ts)
            except ValueError:
                ts = None
            fs = self.create_filesystem_object(snap['parent'])
            Snapshot.objects.get_or_create(
                name=snap['name'],
                timestamp=ts,
                filesystem=fs,
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
        fs, _ = Filesystem.objects.get_or_create(
            name=filesystem.name,
            parent=parent,
            mountpoint=filesystem.is_mounted(),
        )
        return fs

    def create_filesystem_objects(self):
        """
        Convenience method to create Django objects for each filesystem
        """
        filesystems = self.get_all_filesystems()
        for fs in filesystems:
            self.create_filesystem_object(fs)


class FileHelper(object):
    """
    Utility to help walk file trees and process the results for creating File
    objects
    """
    timezone_name = get_default_timezone_name()

    def create_file_object(self, full_path, snapshot=None, directory=False):
        statinfo = os.stat(full_path)
        mtime = datetime.fromtimestamp(statinfo.st_mtime)
        mtime = pytz.timezone(self.timezone_name).localize(mtime)
        try:
            magic_info = magic.from_file(full_path)
        except magic.MagicException:
            magic_info = None
        mime_type = magic.from_file(full_path, mime=True)
        File.objects.get_or_create(
            full_path=full_path,
            snapshot=snapshot,
            directory=directory,
            mime_type=mime_type,
            magic=magic_info,
            modified=mtime,
            size=statinfo.st_size,
        )

    def walk_fs_and_create_files(self, fs_name):
        try:
            fs = Filesystem.objects.get(
                name=fs_name
            )
        except Filesystem.DoesNotExist:
            return
        for dirname, subdirs, files in fs.walk_fs():
            for s in subdirs:
                # TODO: Proper loggin
                print "Creating %s/%s" % (dirname, s)
                self.create_file_object(
                    full_path=u'%s/%s' % (dirname, s),
                    directory=True
                )
            for f in files:
                print "Creating %s/%s" % (dirname, f)
                self.create_file_object(
                    full_path=u'%s/%s' % (dirname, f)
                )
