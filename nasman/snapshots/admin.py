from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sitetree.admin import TreeItemAdmin, override_item_admin

from .models import File, IconMapping


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'dirname', 'mime_type',
                    'modified', 'size',)
    list_display_links = ('name',)
    search_fields = ['full_path', ]


@admin.register(IconMapping)
class IconMappingAdmin(admin.ModelAdmin):
    list_display = ['icon', 'mime_type', ]


class NasmanTreeItemAdmin(TreeItemAdmin):
    fieldsets = (
        (_('Basic settings'), {
            'fields': ('parent', 'title', 'url', 'icon', )
        }),
        (_('Access settings'), {
            'classes': ('collapse',),
            'fields': ('access_loggedin', 'access_guest', 'access_restricted',
                       'access_permissions', 'access_perm_type')
        }),
        (_('Display settings'), {
            'classes': ('collapse',),
            'fields': ('hidden', 'inmenu', 'inbreadcrumbs', 'insitetree')
        }),
        (_('Additional settings'), {
            'classes': ('collapse',),
            'fields': ('hint', 'description', 'alias', 'urlaspattern')
        }),
    )

override_item_admin(NasmanTreeItemAdmin)
