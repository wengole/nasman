from django.conf.urls import patterns, url

from .views.base import DashboardView
from .views.filesystems import FileBrowser, FilesystemList, FilesystemDetail
from .views.filesystems import FilesystemCreate, FilesystemDelete
from .views.filesystems import FilesystemUpdate
from .views.snapshots import SnapshotList, SnapshotCreate


urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name=u'dashboard'),
    url(r'^file-browser$', FileBrowser.as_view(), name=u'file-browser'),
    url(r'^filesystems$', FilesystemList.as_view(), name=u'filesystems'),
    url(r'^filesystem/(?P<pk>\d+)$', FilesystemDetail.as_view(),
        name=u'filesystem'),
    url(r'^filesystem/add$', FilesystemCreate.as_view(),
        name=u'add-fs'),
    url(r'^filesystem/(?P<pk>\d+)/delete$', FilesystemDelete.as_view(),
        name=u'delete-fs'),
    url(r'^filesystem/(?P<pk>\d+)/edit$', FilesystemUpdate.as_view(),
        name=u'edit-fs'),
    url(r'^snapshots$', SnapshotList.as_view(), name=u'snapshots'),
    url(r'^snapshot/add$', SnapshotCreate.as_view(), name=u'add-snap'),
)
