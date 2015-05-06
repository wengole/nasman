from django.db import models
from djorm_pgfulltext.fields import VectorField
from djorm_pgfulltext.models import SearchManager
from fontawesome.fields import IconField
from sitetree.models import TreeItemBase, TreeBase


class File(models.Model):
    """
    Model representing a file/directory/etc on the filesystem
    """
    snapshot_path = models.TextField(
        'snapshot path',
        help_text='The path to the file when the relevant snapshot is mounted')
    original_path = models.TextField(
        'original path',
        help_text='The original path on the filesystem when the snapshot was '
                  'taken'
    )
    snapshot_name = models.TextField(
        'snapshot name',
        help_text='Name of the snapshot'
    )
    path_encoding = models.TextField(
        'path encoding',
        help_text='The filesystem encoding for this file',
        blank=True
    )
    search_index = VectorField()

    objects = SearchManager(
        fields=('snapshot_path', 'original_path'),
        config='pg_catalog.english',
        search_field='search_index',
        auto_update_search_field=True
    )

    class Meta:
        app_label = 'snapshots'


class IconMapping(models.Model):
    """
    Model to manage icon mapping to mimetypes
    """
    icon = IconField(
        'icon',
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

    def __str__(self):
        return self.mime_type


class NasmanTreeItem(TreeItemBase):
    icon = IconField(
        'icon',
        default='circle-o'
    )
