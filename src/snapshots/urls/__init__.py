from django.conf.urls import patterns, include

urlpatterns = patterns(
    '',
    (r'^snapshots/', include('snapshots.urls.snapshot_urls', namespace='snapshots')),
    (r'^files/', include('snapshots.urls.file_urls', namespace='files')),
)
