from django.conf.urls import patterns, url

from .views import HomeView, FileBrowser

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view()),
    url(r'^file-browser$', FileBrowser.as_view(), 'file-browser')
)
