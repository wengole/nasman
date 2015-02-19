from django.conf.urls import patterns, url
from snapshots.views import (SnapshotListView, SnapshotCreateView, SnapshotDetailView,
                     SnapshotUpdateView, SnapshotDeleteView)
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',

    url(r'^create/$',  # NOQA
        login_required(SnapshotCreateView.as_view()),
        name="snapshot_create"),

    url(r'^(?P<pk>\d+)/update/$',
        login_required(SnapshotUpdateView.as_view()),
        name="snapshot_update"),

    url(r'^(?P<pk>\d+)/delete/$',
        login_required(SnapshotDeleteView.as_view()),
        name="snapshot_delete"),

    url(r'^(?P<pk>\d+)/$',
        SnapshotDetailView.as_view(),
        name="snapshot_detail"),

    url(r'^$',
        SnapshotListView.as_view(),
        name="snapshot_list"),
)
