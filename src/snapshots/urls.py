from django.conf.urls import patterns, url

from .views import SnapshotListView


urlpatterns = patterns(
    '',
    url(r'^$', SnapshotListView.as_view(), name='list'),
)
