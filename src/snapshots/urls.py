from django.conf.urls import patterns, url

from .views.base import DashboardView
from .views.filesystems import FileBrowser, FilesystemList, FilesystemDetail
from .views.filesystems import FilesystemCreate, FilesystemDelete
from .views.filesystems import FilesystemUpdate
from .views.search import SnapshotSearchView


urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^file-browser$', FileBrowser.as_view(), name='file-browser'),
    url(r'^filesystems$', FilesystemList.as_view(), name='filesystems'),
    url(r'^filesystem/(?P<pk>\d+)$', FilesystemDetail.as_view(),
        name='filesystem'),
    url(r'^filesystem/add$', FilesystemCreate.as_view(),
        name='add-fs'),
    url(r'^filesystem/(?P<pk>\d+)/delete$', FilesystemDelete.as_view(),
        name='delete-fs'),
    url(r'^filesystem/(?P<pk>\d+)/edit$', FilesystemUpdate.as_view(),
        name='edit-fs'),
    url(r'^search$', SnapshotSearchView.as_view(),
        name='search'),
)
