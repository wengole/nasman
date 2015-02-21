from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^snapshots/', include('snapshots.urls', namespace='snapshots')),
    url(r'^$', include('base.urls')),
    url(r'^search/', include('haystack.urls')),
)
