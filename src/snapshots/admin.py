from django.contrib import admin

from .models import Snapshot, File, Filesystem
# from .tasks import ReindexFilesystem


# def walk_fs_action(modeladmin, request, queryset):
#     for fs in queryset:
#         res=ReindexFilesystem.delay(fs_name=fs.name)
#     return res
# walk_fs_action.short_description = "Reindex selected filesystem(s)"


@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp', 'filesystem',)
    readonly_fields = ['timestamp']

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'dirname', 'mime_type', 'modified', 'size',)
    readonly_fields = []


@admin.register(Filesystem)
class FilesystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'mountpoint', 'parent',)
    list_editable = ['mountpoint', ]
    # actions = [walk_fs_action]
