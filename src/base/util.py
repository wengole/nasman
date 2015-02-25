from django.utils.timezone import get_default_timezone_name
import pytz
import pyzfscore as zfs
from dateutil import parser
from snapshots.models import Snapshot


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
