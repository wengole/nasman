import os
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Snapshot(models.Model):
    """
    Model representing a ZFS snapshot
    """
    name = models.CharField('name', max_length=255)
    timestamp = models.DateTimeField('timestamp', null=True, blank=True)

    class Meta:
        unique_together = ()
        index_together = ()

    def __str__(self):
        return self.name

    @property
    def base_name(self):
        """
        The base name of the snapshot, less the parent filesystem name
        """
        return u'%s' % self.name.split('@')[1]

    @property
    def parent_name(self):
        """
        The parent filesystem name of the snapshot
        """
        return u'%s' % self.name.split('@')[0]

    def walk_snapshot(self):
        """
        os.walk from the snapshot

        :returns: An `os.walk` instance starting from the snapshot
        """
        return os.walk(
            u'/%s/.zfs/snapshot/%s' % (
                self.parent_name,
                self.base_name
            )
        )


@python_2_unicode_compatible
class File(models.Model):
    """
    Model representing a file/directory/etc on the filesystem
    """
    full_path = models.CharField('full path', max_length=255)
    snapshot = models.ForeignKey(
        Snapshot,
        verbose_name='snapshot',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    mime_type = models.CharField('mime type', blank=True, max_length=255)
    extension = models.CharField('extension', blank=True, max_length=255)
    created = models.DateTimeField('created')
    modified = models.DateTimeField('modified')
    size = models.IntegerField('size', blank=True, null=True)

    class Meta:
        unique_together = ()
        index_together = ()

    def __str__(self):
        return self.full_path