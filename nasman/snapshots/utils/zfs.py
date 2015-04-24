from datetime import datetime
import logging
from subprocess import check_output, CalledProcessError

import pytz

from ..base import BaseUtil, BaseFilesystem, BaseSnapshot


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
        output = check_output(cmd)
    except CalledProcessError:
        logger.error('Failed to pass command %s', ' '.join(cmd))
        return []
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
        return self.basename

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
        The mountpoint of this snapshot (if it is mounted)
        """
        fs = ZFSUtil.get_filesystem(self.parent_name)
        return fs.mountpoint

    def __repr__(self):
        return self.name


class ZFSFilesystem(BaseFilesystem):
    """
    ZFS Filesystem object definition
    """
    @property
    def mountpoint(self):
        """
        The mountpoint of this filesystem as defined within ZFS
        """
        return self._mountpoint

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
        parsed = _parse_cmd_output(
            ['zfs', 'get', 'mounted', '-H', self.name]
        )
        return True if parsed[0][2] == 'yes' else False

    def mount(self):
        """
        If this file system is not already mounted, mount it using ZFS
        :return: Whether the filesystem is now mounted (False on error)
        :rtype: bool
        """
        if self.is_mounted:
            return True
        parsed = _parse_cmd_output(
            ['zfs', 'mount', self.name]
        )
        return False if parsed is None else True

    def __repr__(self):
        return self.name


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

