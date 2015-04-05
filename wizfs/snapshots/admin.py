from django.contrib import admin

from snapshots.models import Snapshot, File, Filesystem, IconMapping


@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp', 'filesystem',)
    readonly_fields = ['timestamp']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'dirname', 'mime_type',
                    'modified', 'size',)
    list_display_links = ('name',)
    search_fields = ['full_path', ]


@admin.register(Filesystem)
class FilesystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'mountpoint', 'parent',)
    list_editable = ['mountpoint', ]
    actions = ['walk_fs_action']
    search_fields = ['name', ]


@admin.register(IconMapping)
class IconMappingAdmin(admin.ModelAdmin):
    list_display = ['icon', 'mime_type', ]
