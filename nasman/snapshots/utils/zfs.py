from datetime import datetime
import logging
from subprocess import check_output, CalledProcessError

import pytz

from ..base import BaseUtil, BaseFilesystem, BaseSnapshot


logger = logging.getLogger(__name__)


def _parse_cmd_output(cmd):
    try:
        output = check_output(cmd)
    except CalledProcessError:
        logger.error('Failed to pass command %s', ' '.join(cmd))
        return None
    return [x.split() for x in output.decode('utf-8').splitlines()]


class ZFSSnapshot(BaseSnapshot):
    @property
    def filesystem(self):
        return self.basename

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def name(self):
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
        fs = ZFSUtil.get_filesystem(self.parent_name)
        return fs.mountpoint


class ZFSFilesystem(BaseFilesystem):
    @property
    def mountpoint(self):
        return self._mountpoint

    @property
    def name(self):
        return self._name


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

