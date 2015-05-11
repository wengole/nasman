from django.conf.urls import patterns, url

from .views import Notifications


urlpatterns = patterns(
    '',
    url(r'^$', Notifications.as_view(), name='home'),
)
