"""
Snapshot app views
"""
from braces.views import SetHeadlineMixin, MessageMixin, AjaxResponseMixin, \
    JSONResponseMixin
from django.shortcuts import redirect
from vanilla import TemplateView, ListView, DetailView, CreateView

from .models import File, Filesystem
from .tasks import reindex_filesystem
from wizfs.celery import app


class DashboardView(JSONResponseMixin, AjaxResponseMixin, SetHeadlineMixin, TemplateView):
    """
    View for the homepage
    """
    http_method_names = [u'get']
    template_name = u'dashboard.html'
    headline = u'WiZFS Dashboard'

    def get_ajax(self, request, *args, **kwargs):
        inspector = app.control.inspect()
        tasks = inspector.active()
        return self.render_json_response({'tasks': tasks})


class FileBrowser(SetHeadlineMixin, ListView):
    model = File
    headline = u'File Browser'


class FilesystemList(SetHeadlineMixin, ListView):
    model = Filesystem
    headline = u'ZFS Filesystems'


class FilesystemDetail(MessageMixin, SetHeadlineMixin, DetailView):
    model = Filesystem

    def get_headline(self):
        return u'%s Filesystem Details' % self.get_object().name

    def get(self, request, *args, **kwargs):
        if request.GET.get(u'reindex'):
            fs = self.get_object()
            reindex_filesystem.delay(fs.name)
            self.messages.info(u'Reindex of %s started' % fs.name)
            return redirect(u'wizfs:dashboard')
        return super(FilesystemDetail, self).get(request, *args, **kwargs)


class FilesystemCreate(SetHeadlineMixin, CreateView):
    model = Filesystem
    fields = [u'name', u'mountpoint', u'parent']
    headline = u'Add New Filesystem'
