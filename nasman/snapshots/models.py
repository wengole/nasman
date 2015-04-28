from datetime import datetime
from pathlib import Path

from django.db import models
from django.utils.timezone import get_default_timezone_name
from djorm_pgfulltext.fields import VectorField
from djorm_pgfulltext.models import SearchManager
from fontawesome.fields import IconField
import magic
import pytz
from sitetree.models import TreeItemBase, TreeBase



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

    objects = SearchManager(
        fields=('name', 'dirname', 'snapshot_name', 'magic'),
        config='pg_catalog.english',
        search_field='search_index',
        auto_update_search_field=True
    )

    class Meta:
        app_label = 'snapshots'

    def clean_fields(self, exclude=None):
        path_field = self._meta.get_field('full_path')
        self.full_path = path_field.clean(self.full_path, self)
        self.dirname = str(self.full_path.parent)
        self.name = str(self.full_path.name)
        self.directory = self.full_path.is_dir()
        try:
            mime_type = magic.from_file(
                str(self.full_path), mime=True).decode('utf-8')
            self.magic = magic.from_file(
                str(self.full_path)).decode('utf-8')
        except magic.MagicException:
            icon = None
            self.magic = ''
        else:
            icon, _ = IconMapping.objects.get_or_create(
                mime_type=mime_type
            )
        self.mime_type = icon
        mtime = datetime.fromtimestamp(self.full_path.lstat().st_mtime)
        mtime = pytz.timezone(get_default_timezone_name()).localize(mtime)
        self.modified = mtime
        self.size = self.full_path.lstat().st_size
        super(File, self).clean_fields(exclude)

    def __unicode__(self):
        return self.full_path

    @property
    def extension(self):
        """
        The file extension of this file
        :rtype: str
        """
        return self.full_path.suffix


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


class NasmanTree(TreeBase):
    pass


class NasmanTreeItem(TreeItemBase):
    icon = IconField(
        'icon',
        default='circle-o'
    )
