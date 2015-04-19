from django.contrib import admin

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
