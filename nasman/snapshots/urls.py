from django.conf.urls import patterns, url

from .views.base import DashboardView
from .views.filesystems import FileBrowser, FilesystemList
from .views import snapshots as snaps


urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^file-browser$', FileBrowser.as_view(), name='file-browser'),
    url(r'^filesystems$', FilesystemList.as_view(), name='filesystems'),
    # url(r'^filesystem/add$', FilesystemList.as_view(), name='filesystems'),
    url(r'^snapshots$', snaps.SnapshotList.as_view(), name='snapshots'),
    url(r'^snapshots/refresh$', snaps.SnapshotList.as_view(refresh=True),
        name='snapshots-refresh'),
    url(r'^snapshot/add$', snaps.SnapshotCreate.as_view(), name='add-snap'),
    url(r'^snapshot/(?P<name>[\w\d@\-:.\/]+)/reindex$',
        snaps.SnapshotReindex.as_view(),
        name='reindex-snap'),
    url(r'^snapshot/(?P<name>[\w\d@\-:.\/]+)/mount$',
        snaps.SnapshotMount.as_view(),
        name='mount-snap'),
)
