from django.conf.urls import patterns, url

from .views.base import DashboardView
from .views.filesystems import FileBrowser, FilesystemList
from .views.snapshots import SnapshotList, SnapshotCreate, SnapshotReindex


urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^file-browser$', FileBrowser.as_view(), name='file-browser'),
    url(r'^filesystems$', FilesystemList.as_view(), name='filesystems'),
    url(r'^snapshots$', SnapshotList.as_view(), name='snapshots'),
    url(r'^snapshot/add$', SnapshotCreate.as_view(), name='add-snap'),
    url(r'^snapshot/(?P<name>[\w\d@\-:.\/]+)$',
        SnapshotReindex.as_view(),
        name='reindex-snap'),
)
