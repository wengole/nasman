from django.conf.urls import patterns, include

urlpatterns = patterns('',

    (r'^snapshots/', include('snapshots.urls.snapshot_urls')),  # NOQA
    (r'^files/', include('snapshots.urls.file_urls')),
)
