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
        pool = zfs.ZPool.list()[0]
        fs = pool.to_filesystem()
        return fs

    def get_snapshots(self):
        fs = self._get_pool_as_filesystem()
        snapshots = fs.iter_snapshots_sorted()
        return [x.name for x in snapshots]
