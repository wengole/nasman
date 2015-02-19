from django.conf.urls import patterns, url
from snapshots.views import (FileListView, FileCreateView, FileDetailView,
                             FileUpdateView, FileDeleteView)
from django.contrib.auth.decorators import login_required


urlpatterns = patterns(
    '',
    url(r'^create/$',
        login_required(FileCreateView.as_view()),
        name="file_create"),

    url(r'^(?P<pk>\d+)/update/$',
        login_required(FileUpdateView.as_view()),
        name="file_update"),

    url(r'^(?P<pk>\d+)/delete/$',
        login_required(FileDeleteView.as_view()),
        name="file_delete"),

    url(r'^(?P<pk>\d+)/$',
        FileDetailView.as_view(),
        name="file_detail"),

    url(r'^$',
        FileListView.as_view(),
        name="file_list"),
)
