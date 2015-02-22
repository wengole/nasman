import pyzfscore as zfs


class ZFSHelper(object):
    """
    Helper utility for accessing ZFS features
    """
    def _get_pool_as_filesystem(self):
        """
        Get the first available `ZPool` object and return it as a `ZFilesystem`

        :return: The first available pool as a filesystem
        :rtype: `ZFilesystem`
        """
        return zfs.ZPool.list()[0].filesystem

    def get_snapshots(self):
        poolfs = self._get_pool_as_filesystem()
        snapshots = poolfs.iter_snapshots_sorted
        return [x for x in snapshots]
