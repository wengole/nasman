"""
Snapshot app views
"""
from braces.views import SetHeadlineMixin, MessageMixin, AjaxResponseMixin, \
    JSONResponseMixin
from celery import Celery
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.core.cache import cache
from snapshots.utils import ZFSHelper
from vanilla import TemplateView, ListView, DetailView, CreateView, DeleteView

from .forms import FilesystemForm
from .models import File, Filesystem
from .tasks import reindex_filesystem

app = Celery('wizfs')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


class DashboardView(JSONResponseMixin, AjaxResponseMixin, SetHeadlineMixin, TemplateView):
    """
    View for the homepage
    """
    http_method_names = [u'get']
    template_name = u'dashboard.html'
    headline = u'WiZFS Dashboard'

    def get_ajax(self, request, *args, **kwargs):
        """
        AJAX call to get reindex task status

        :return: JSON list of tasks
        """
        result = cache.get(u'reindex_result')
        json_dict = {'state': 'NOTFOUND',
                     'progress': 0.0,
                     'total': 0,
                     'done': 0}
        if result is None:
            return self.render_json_response(json_dict)
        json_dict['state'] = result.state
        if result.state == 'PROGRESS':
            json_dict['progress'] = result.info['percentage']
            json_dict['total'] = result.info['total']
            json_dict['done'] = result.info['done']
        elif result.state == 'SUCCESS':
            json_dict['progress'] = 100.0
        return self.render_json_response(json_dict)


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
        """
        If "reindex" query parameter passed, then reindex the chosen filesystem
        """
        if request.GET.get(u'reindex'):
            fs = self.get_object()
            reindex_result = reindex_filesystem.delay(fs.name)
            cache.set(u'reindex_result', reindex_result, None)
            self.messages.info(u'Reindex of %s started' % fs.name)
            return redirect(u'wizfs:dashboard')
        return super(FilesystemDetail, self).get(request, *args, **kwargs)


class FilesystemCreate(MessageMixin, SetHeadlineMixin, CreateView):
    model = Filesystem
    fields = [u'name', u'mountpoint', u'parent']
    headline = u'Add New Filesystem'
    form_class = FilesystemForm

    def get(self, request, *args, **kwargs):
        """
        If "auto" query parameter is passed then use utility to add all found
        filesystems
        """
        if request.GET.get(u'auto'):
            util = ZFSHelper()
            util.create_filesystem_objects()
            self.messages.info(u'Added all filesystems automatically')
            return redirect(u'wizfs:filesystems')
        return super(FilesystemCreate, self).get(request, *args, **kwargs)


class FilesystemDelete(SetHeadlineMixin, DeleteView):
    model = Filesystem
    success_url = reverse_lazy('wizfs:filesystems')

    def get_headline(self):
        return u'Delete %s filesystem?' % self.get_object().name
