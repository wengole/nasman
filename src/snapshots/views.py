"""
Snapshot app views
"""
from braces.views import (SetHeadlineMixin, MessageMixin, AjaxResponseMixin,
                          JSONResponseMixin)
from celery import Celery
from celery import states
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.core.cache import cache
from vanilla import TemplateView, ListView, DetailView, CreateView, DeleteView, \
    UpdateView

from .utils import ZFSHelper
from .forms import FilesystemForm
from .models import File, Filesystem
from .tasks import reindex_filesystem


app = Celery('wizfs')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


def get_status_dict(fs):
    status = fs.reindex_status
    json_dict = {'state': 'NOTFOUND',
                 'progress': 0.0,
                 'total': 0,
                 'done': 0}
    if status is None:
        return json_dict
    json_dict['state'] = status.state
    if status.state in [states.FAILURE, states.PENDING]:
        return json_dict
    json_dict['progress'] = status.info.get('percentage', 0)
    json_dict['total'] = status.info.get('total', 0)
    json_dict['done'] = status.info.get('done', 0)
    return json_dict


class DashboardView(JSONResponseMixin, AjaxResponseMixin, SetHeadlineMixin,
                    TemplateView):
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


class FilesystemList(JSONResponseMixin, AjaxResponseMixin, SetHeadlineMixin,
                     ListView):
    model = Filesystem
    headline = u'ZFS Filesystems'

    def get_ajax(self, request, *args, **kwargs):
        filesystems = []
        for fs in self.get_queryset().all():
            json_dict = get_status_dict(fs)
            json_dict['id'] = fs.id
            filesystems.append(json_dict)
        return self.render_json_response({
            'filesystems': filesystems
        })


class FilesystemDetail(JSONResponseMixin, AjaxResponseMixin, MessageMixin,
                       SetHeadlineMixin, DetailView):
    model = Filesystem

    def get_headline(self):
        return u'%s Filesystem Details' % self.get_object().name

    def get(self, request, *args, **kwargs):
        """
        If "reindex" query parameter passed, then reindex the chosen filesystem
        """
        if request.GET.get(u'reindex'):
            fs = self.get_object()
            status = fs.reindex_status
            if status is None or status.state in states.READY_STATES or status.state is None:
                fs.reindex_status = reindex_filesystem.delay(fs.name)
                self.messages.info(u'Reindex of %s started' % fs.name)
                return redirect(u'wizfs:filesystems')
            self.messages.warning(
                u'Reindex of %s already in progress' % fs.name)
            return redirect(u'wizfs:filesystems')
        return super(FilesystemDetail, self).get(request, *args, **kwargs)

    def get_ajax(self, request, *args, **kwargs):
        fs = self.get_object()
        json_dict = get_status_dict(fs)
        return self.render_json_response(json_dict)


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
    success_url = reverse_lazy(u'wizfs:filesystems')

    def get_headline(self):
        return u'Delete %s filesystem?' % self.get_object().name


class FilesystemUpdate(SetHeadlineMixin, UpdateView):
    model = Filesystem
    success_url = reverse_lazy(u'wizfs:filesystems')
    form_class = FilesystemForm

    def get_headline(self):
        return u'Edit %s filesystem' % self.get_object().name
