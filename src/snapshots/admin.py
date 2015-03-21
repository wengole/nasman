import logging

from haystack.admin import SearchChangeList
from django.conf import settings
from django.contrib import admin
from haystack.query import SearchQuerySet

from .models import Snapshot, File, Filesystem
from .tasks import reindex_filesystem


logger = logging.getLogger(__name__)


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

    def get_search_results(self, request, queryset, search_term):
        sqs = SearchQuerySet().auto_query(request.GET['q']).facet('directory')
        return sqs, False

    def get_changelist(self, request, **kwargs):
        return SearchChangeList

    def changelist_view(self, request, extra_context=None):
        sqs, _ = self.get_search_results(request, None, 'snapshot')
        extra_context = {
            'facets': sqs.query.get_facet_counts()
        }
        return super(FileAdmin, self).changelist_view(request, extra_context)

@admin.register(Filesystem)
class FilesystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'mountpoint', 'parent',)
    list_editable = ['mountpoint', ]
    actions = ['walk_fs_action']
    search_fields = ['name', ]

    def walk_fs_action(self, request, queryset):
        logger.info(settings)
        for fs in queryset:
            res = reindex_filesystem.delay(fs_name=fs.name)

    walk_fs_action.short_description = "Reindex selected filesystem(s)"

