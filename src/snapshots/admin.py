import logging
from haystack.admin import SearchModelAdmin
from django.conf import settings
from django.contrib import admin

from .models import Snapshot, File, Filesystem
from .tasks import reindex_filesystem


logger = logging.getLogger(__name__)


@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp', 'filesystem',)
    readonly_fields = ['timestamp']


@admin.register(File)
class FileAdmin(SearchModelAdmin):
    list_display = ('name', 'dirname', 'mime_type', 'modified', 'size',)
    readonly_fields = []


@admin.register(Filesystem)
class FilesystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'mountpoint', 'parent',)
    list_editable = ['mountpoint', ]
    actions = ['walk_fs_action']

    def walk_fs_action(self, request, queryset):
        logger.info(settings)
        for fs in queryset:
            res = reindex_filesystem.delay(fs_name=fs.name)

    walk_fs_action.short_description = "Reindex selected filesystem(s)"

