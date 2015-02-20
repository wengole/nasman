from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static

from .views import HomeView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view()),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
