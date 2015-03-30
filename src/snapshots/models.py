from django import forms
from django.core.cache import cache
import os
from django.core.urlresolvers import reverse_lazy
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
        return reverse_lazy('wizfs:filesystem', kwargs={'pk': self.pk})

    def walk_fs(self):
        """
        os.walk from the filesystem mountpoint

        :returns: An `os.walk` instance starting from the mountpoint
        """
        return os.walk(self.mountpoint.encode('utf-8'))

    @property
    def reindex_cache_key(self):
        """
        Cache key for reindex job
        """
        return u'reindex_%s_status' % self.name

    @property
    def reindex_status(self):
        """
        Gets the cached `AsyncResult` of a reindex job
        """
        status = cache.get(self.reindex_cache_key)
        return status

    @reindex_status.setter
    def reindex_status(self, status):
        """
        Sets the cached `AsyncResult` of a reindex job
        """
        cache.set(self.reindex_cache_key, status, None)


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
    full_path = models.TextField(u'full path')
    dirname = models.TextField(
        u'dirname',
        db_index=True
    )
    name = models.TextField(u'name')
    snapshot = models.ForeignKey(
        Snapshot,
        verbose_name=u'snapshot',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    directory = models.BooleanField(default=False)
    mime_type = models.ForeignKey(
        u'IconMapping',
        verbose_name=u'mime-type',
        on_delete=models.SET_NULL,
        null=True
    )
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


@python_2_unicode_compatible
class IconMapping(models.Model):
    """
    Model to manage icon mapping to mimetypes
    """
    ICON_CHOICES = (
        ('fa-file-o', 'default'),
        ('fa-file-archive-o', 'archive'),
        ('fa-file-audio-o', 'audio'),
        ('fa-file-code-o', 'code'),
        ('fa-file-excel-o', 'excel'),
        ('fa-file-image-o', 'image'),
        ('fa-file-pdf-o', 'pdf'),
        ('fa-file-powerpoint-o', 'powerpoint'),
        ('fa-file-text-o', 'text'),
        ('fa-file-video-o', 'video'),
        ('fa-file-word-o', 'word'),
        ('fa-folder-open-o', 'directory')
    )
    icon = models.CharField(
        u'icon',
        max_length=25,
        choices=ICON_CHOICES,
        default='fa-file-o'
    )
    mime_type = models.CharField(
        u'mime-type',
        max_length=255,
        primary_key=True,
        db_index=True
    )

    def __str__(self):
        return self.mime_type
