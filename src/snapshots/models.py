from django.core.urlresolvers import reverse
import os
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Filesystem(models.Model):
    """
    Model representing ZFS Filesystem
    """
    name = models.CharField(u'name', max_length=255, unique=True)
    parent = models.ForeignKey(
        u'self',
        related_name=u'children',
        null=True,
        blank=True
    )
    mountpoint = models.CharField(u'mountpoint', max_length=255, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wizfs:filesystem', kwargs={'pk': self.pk})

    def walk_fs(self):
        """
        os.walk from the filesystem mountpoint

        :returns: An `os.walk` instance starting from the mountpoint
        """
        return os.walk(
            u'%s/' % (
                self.mountpoint,
            )
        )


@python_2_unicode_compatible
class Snapshot(models.Model):
    """
    Model representing a ZFS snapshot
    """
    name = models.CharField(u'name', max_length=255)
    timestamp = models.DateTimeField(u'timestamp', null=True, blank=True)
    filesystem = models.ForeignKey(u'Filesystem', related_name=u'snapshots')

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
        return u'%s' % self.name.split(u'@')[1]

    @property
    def parent_name(self):
        """
        The parent filesystem name of the snapshot
        """
        return u'%s' % self.name.split(u'@')[0]

    def walk_snapshot(self):
        """
        os.walk from the snapshot

        :returns: An `os.walk` instance starting from the snapshot
        """
        return os.walk(
            u'%s/.zfs/snapshot/%s' % (
                self.filesystem.mountpoint,
                self.base_name
            )
        )


@python_2_unicode_compatible
class File(models.Model):
    """
    Model representing a file/directory/etc on the filesystem
    """
    full_path = models.CharField(u'full path', max_length=255)
    snapshot = models.ForeignKey(
        Snapshot,
        verbose_name=u'snapshot',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    directory = models.BooleanField(default=False)
    mime_type = models.CharField(u'mime type', blank=True, max_length=255)
    magic = models.CharField(u'magic', blank=True, max_length=255)
    modified = models.DateTimeField(u'modified')
    size = models.IntegerField(u'size', blank=True, null=True)

    class Meta:
        unique_together = ()
        index_together = ()

    def __str__(self):
        return self.full_path

    @property
    def extension(self):
        """
        The file extension of this file
        :rtype: str
        """
        _, extension = os.path.splitext(self.full_path)
        return extension

    @property
    def dirname(self):
        """
        The directory containing this file
        :rtype: str
        """
        return os.path.dirname(self.full_path)

    @property
    def name(self):
        """
        The filename of this file
        :rtype: str
        """
        return os.path.basename(self.full_path)
