from django.conf.urls import patterns, url

from .views import DashboardView, FileBrowser

urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^file-browser$', FileBrowser.as_view(), name='file-browser')
)
