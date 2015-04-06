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

    def save(self, **kwargs):
        self.mountpoint = os.path.normpath(self.mountpoint)
        super(Filesystem, self).save(**kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('wizfs:filesystem', kwargs={'pk': self.pk})


@python_2_unicode_compatible
class Snapshot(models.Model):
    """
    Model representing a ZFS snapshot
    """
    name = models.CharField(u'name', max_length=255, unique=True)
    timestamp = models.DateTimeField(
        u'timestamp',
        null=True,
        auto_now_add=True
    )
    filesystem = models.ForeignKey(u'Filesystem', related_name=u'snapshots')

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

    @property
    def mountpoint(self):
        return os.path.join(
            self.filesystem.mountpoint,
            self.base_name
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

    def save(self, **kwargs):
        self.full_path = os.path.normpath(self.full_path)
        self.dirname = os.path.normpath(self.dirname)
        super(File, self).save(**kwargs)

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

    def save(self, **kwargs):
        icon_mapping = {x[1]: x[0] for x in self.ICON_CHOICES}
        if self.icon == 'fa-file-o':
            major = self.mime_type.split('/')[0]
            if major in icon_mapping:
                self.icon = icon_mapping[major]
        super(IconMapping, self).save(**kwargs)

    def __str__(self):
        return self.mime_type
