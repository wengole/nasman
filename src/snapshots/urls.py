from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^file-browser$', views.FileBrowser.as_view(), name='file-browser'),
    url(r'^filesystems$', views.FilesystemList.as_view(), name='filesystems'),
    url(r'^filesystem/(?P<pk>\d+)$', views.FilesystemDetail.as_view(),
        name='filesystem'),
    url(r'^filesystem/add$', views.FilesystemCreate.as_view(),
        name='add-fs'),
)
