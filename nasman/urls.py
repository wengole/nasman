from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^snapshots/', include('nasman.snapshots.urls',
                                namespace='snapshots')),
    url(r'^', include('nasman.core.urls', namespace='core'))
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
