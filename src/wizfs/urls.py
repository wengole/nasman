from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from snapshots.views import SnapshotSearch


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    # url(r'^snapshots/', include('snapshots.urls', namespace='snapshots')),
    # url(r'^$', include('base.urls')),
    url(r'^search/?$', SnapshotSearch.as_view(), name='search'),
)
