from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('base.urls', namespace='base')),
)
