import os

from django.db import models
from djorm_pgfulltext.fields import VectorField
from djorm_pgfulltext.models import SearchManager
from pathlib import Path


class PathField(models.TextField):

    description = 'A path on a filesystem.'

    def to_python(self, value):
        if value is None:
            return value
        return Path(value)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return Path(value)


class File(models.Model):
    """
    Model representing a file/directory/etc on the filesystem
    """
    full_path = PathField('full path')
    dirname = models.TextField(
        'dirname',
        db_index=True
    )
    name = models.TextField('name', db_index=True)
    snapshot_name = models.TextField('snapshot', db_index=True)
    directory = models.BooleanField(default=False)
    mime_type = models.ForeignKey(
        'IconMapping',
        verbose_name='mime-type',
        on_delete=models.SET_NULL,
        null=True
    )
    magic = models.CharField('magic', blank=True, max_length=255)
    modified = models.DateTimeField('modified')
    size = models.IntegerField('size', blank=True, null=True)
    search_index = VectorField()

    class Meta:
        app_label = 'snapshots'

    def __unicode__(self):
        return self.full_path

    @property
    def extension(self):
        """
        The file extension of this file
        :rtype: str
        """
        return self.full_path.suffix

    objects = SearchManager(
        fields=('name', 'dirname', 'snapshot_name', 'magic'),
        config='pg_catalog.english',
        search_field='search_index',
        auto_update_search_field=True
    )


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
        'icon',
        max_length=25,
        choices=ICON_CHOICES,
        default='fa-file-o'
    )
    mime_type = models.CharField(
        'mime-type',
        max_length=255,
        primary_key=True,
        db_index=True
    )

    class Meta:
        app_label = 'snapshots'

    def save(self, **kwargs):
        icon_mapping = {x[1]: x[0] for x in self.ICON_CHOICES}
        if self.icon == 'fa-file-o':
            major = self.mime_type.split('/')[0]
            if major in icon_mapping:
                self.icon = icon_mapping[major]
        super(IconMapping, self).save(**kwargs)

    def __str__(self):
        return self.mime_type
