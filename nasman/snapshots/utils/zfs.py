from datetime import datetime
import logging
from subprocess import check_output, CalledProcessError, STDOUT
from pathlib import Path
from django.core.cache import cache

import pytz

from .base import BaseUtil, BaseFilesystem, BaseSnapshot


logger = logging.getLogger(__name__)


def _parse_cmd_output(cmd):
    """
    Run the given arguments as a subprocess, and spilt the output into lines
    and columns
    :param cmd: The command arguments to run
    :type cmd: list
    :return: The parsed output
    :rtype: list
    """
    try:
        output = check_output(cmd, stderr=STDOUT)
    except CalledProcessError as e:
        logger.error('Failed to pass command %s', ' '.join(cmd))
        logger.error('Output was %s', e.output)
        raise
    return [x.split() for x in output.decode('utf-8').splitlines()]


class ZFSSnapshot(BaseSnapshot):
    """
    ZFS Snapshot object definition
    """
    @property
    def filesystem(self):
        """
        The filesystem this is a snapshot of
        """
        return ZFSUtil.get_filesystem(self.parent_name)

    @property
    def timestamp(self):
        """
        The `datetime` this snapshot was created (according to ZFS)
        """
        return self._timestamp

    @property
    def name(self):
        """
        The name of this snapshot
        """
        return self._name

    @property
    def basename(self):
        """
        The base name of the snapshot, less the parent filesystem name
        """
        return self.name.split('@')[1]

    @property
    def parent_name(self):
        """
        The parent filesystem name of the snapshot
        """
        return self.name.split('@')[0]

    @property
    def mountpoint(self):
        """
        The mountpoint of this snapshot (generated by NASMan)
        """
        return Path('/tmp/zfs/snapshot/{}'.format(self.name))

    @property
    def is_mounted(self):
        """
        Whether this snapshot is currently mounted
        """
        parsed = _parse_cmd_output(
            ['mount']
        )
        mounts = [x[0] for x in parsed]
        return self.name in mounts

    def mount(self):
        """
        If this snapshot is not already mounted, mount it under /tmp
        """
        if self.is_mounted:
            return True
        mountpoint = self.mountpoint
        if not mountpoint.exists():
            self.mountpoint.mkdir(parents=True)
        parsed = _parse_cmd_output(
            ['mount', '-tzfs', self.name, str(mountpoint)]
        )
        return True

    def unmount(self):
        """
        If this snapshot it mounted, unmount it
        """
        if not self.is_mounted:
            return True
        mountpoint = self.mountpoint
        parsed = _parse_cmd_output(
            ['umount', str(mountpoint)]
        )
        return True

    def __repr__(self):
        return self.name

    def __iter__(self):
        d = {'name': self.name, 'timestamp': self.timestamp}
        for key, value in d.items():
            yield (key, value)


class ZFSFilesystem(BaseFilesystem):
    """
    ZFS Filesystem object definition
    """
    @property
    def mountpoint(self):
        """
        The mountpoint of this filesystem as defined within ZFS
        """
        return '/host_root{}'.format(self._mountpoint)

    @property
    def name(self):
        """
        Name of this filesystem
        """
        return self._name

    @property
    def is_mounted(self):
        """
        Whether this filesystem is currently mounted
        """
        return self.mount()

    def mount(self):
        """
        If this file system is not already mounted, mount it using ZFS
        """
        try:
            _parse_cmd_output(
                ['zfs', 'mount', self.name]
            )
        except CalledProcessError as e:
            if 'already mounted' in str(e.output):
                return True
            raise
        return True

    def unmount(self):
        """
        If this filesystem is mounted, unmount it using ZFS
        """
        if not self.is_mounted:
            return True
        parsed = _parse_cmd_output(
            ['zfs', 'unmount', self.name]
        )
        return True

    def __repr__(self):
        return self.name

    def __iter__(self):
        d = {'name': self.name, 'mountpoint': self.mountpoint}
        for key, value in d.items():
            yield (key, value)


class ZFSUtil(BaseUtil):
    """
    Helper utility for accessing ZFS features
    """

    @classmethod
    def get_filesystems(cls):
        """
        Gets a list of filesystems
        :return: A list of `ZFSFilesystem` objects
        :rtype: list
        """
        parsed = _parse_cmd_output(
            ['zfs', 'list', '-Hp', '-tfilesystem', '-oname,mountpoint']
        )
        if parsed is None:
            return None
        filesystems = []
        for fs in parsed:
            filesystems.append(
                ZFSFilesystem(
                    fs[0],
                    fs[1]
                )
            )
        return filesystems

    @classmethod
    def get_snapshots(cls):
        """
        Gets a list of snapshots
        :return: A list of `ZFSSnapshot`
        :rtype: list
        """
        parsed = _parse_cmd_output(
            ['zfs', 'list', '-Hp', '-tsnap', '-oname,creation']
        )
        if parsed is None:
            return None
        snaps = []
        for snap in parsed:
            ts = datetime.fromtimestamp(int(snap[1]))
            ts = pytz.timezone(cls.timezone_name).localize(ts)
            snaps.append(
                ZFSSnapshot(
                    snap[0],
                    ts
                )
            )
        return snaps

    @classmethod
    def get_filesystem(cls, fs_name):
        """
        Gets a filesystem by name
        :param fs_name: Name of the filesystem to get
        :type fs_name: basestring
        :return: A `ZFSFilesystem`
        :rtype: `nasman.snapshots.zfs.ZFSFilesystem`
        """
        parsed = _parse_cmd_output(
            ['zfs',
             'list',
             '-Hp',
             '-tfilesystem',
             '-oname,mountpoint',
             fs_name]
        )
        if parsed is None:
            return None
        return ZFSFilesystem(parsed[0][0], parsed[0][1])

    @classmethod
    def get_snapshot(cls, snap_name):
        """
        Gets a snapshot by name
        :param snap_name: Name of the snapshot to get
        :type snap_name: basestring
        :return: A `ZFSSnapshot`
        :rtype: `nasman.snapshots.zfs.ZFSSnapshot`
        """
        parsed = _parse_cmd_output(
            ['zfs',
             'list',
             '-Hp',
             '-tsnap',
             '-oname,creation',
             snap_name]
        )
        if parsed is None:
            return None
        return ZFSSnapshot(parsed[0][0], parsed[0][1])

    @classmethod
    def create_snapshot(cls, snap_name, fs_name, recurse):
        """
        Creates a snapshot
        :param snap_name: Name of the snapshot to create
        :type snap_name: str
        :param fs_name: Name of the filesystem to take snapshot of
        :type fs_name: str
        :param recurse: Whether to recurse filesystems
        :type recurse: bool
        :return: The snapshot just created
        :rtype: `nasman.snapshots.zfs.ZFSSnapshot`
        """
        cache.delete('zfs-snapshots')
        full_name = '{0}@{1}'.format(
            fs_name,
            snap_name
        )
        cmd = ['zfs',
               'snapshot',
               full_name
               ]
        if recurse:
            cmd.append('-r')
        parsed = _parse_cmd_output(cmd)
        if parsed is None:
            return None
        return cls.get_snapshot(full_name)
