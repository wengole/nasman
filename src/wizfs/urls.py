from django.conf.urls import patterns, include, url
from django.contrib import admin

from base.views import HomeView

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^snapshots/', include('snapshots.urls')),
    url(r'^$', include('base.urls')),
)
