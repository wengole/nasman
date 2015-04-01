"""
Snapshot app views
"""
from collections import defaultdict
from datetime import datetime
import magic
import os
from braces.views import (JSONResponseMixin,
                          AjaxResponseMixin,
                          SetHeadlineMixin, MessageMixin)
from celery import Celery
from celery import states
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from haystack.generic_views import FacetedSearchView
from haystack.query import SearchQuerySet
from vanilla import (TemplateView,
                     ListView,
                     DetailView,
                     CreateView,
                     DeleteView,
                     UpdateView)

from .mixins import SearchFormMixin
from .utils import ZFSHelper
from .forms import FilesystemForm, CrispyFacetedSearchForm
from .models import File, Filesystem, Snapshot, IconMapping
from .tasks import reindex_filesystem


app = Celery('wizfs')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


def get_status_dict(fs):
    status = fs.reindex_status
    json_dict = {'state': 'NOTFOUND', 'progress': 0.0, 'total': 0, 'done': 0}
    if status is None:
        return json_dict
    json_dict['state'] = status.state
    if status.state in [states.FAILURE, states.PENDING]:
        return json_dict
    json_dict['progress'] = status.info.get('percentage', 0)
    json_dict['total'] = status.info.get('total', 0)
    json_dict['done'] = status.info.get('done', 0)
    return json_dict


class FileBrowser(BaseView, TemplateView):
    """
    Browse live filesystem using python os stblib
    """
    template_name = u'snapshots/file_list.html'
    headline = u'File Browser'
    fs = None
    path = None
    snapshot = None

    def get(self, request, *args, **kwargs):
        fs_name = self.request.GET.get(u'fs')
        snap_name = self.request.GET.get(u'snap')
        self.path = self.request.GET.get(u'path')
        if fs_name is not None:
            self.fs = get_object_or_404(Filesystem, name=fs_name)
        else:
            self.fs = Filesystem.objects.first()
            if self.fs is None:
                raise Http404(u'No Filesystems yet. Please add one')
        if snap_name is not None:
            self.snapshot = get_object_or_404(Snapshot, name=snap_name)
        else:
            self.snapshot = Snapshot.objects.first()
        return super(FileBrowser, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FileBrowser, self).get_context_data(**kwargs)
        if self.path is None:
            self.path = self.fs.mountpoint
        self.path = os.path.normpath(self.path)
        icon_mapping = defaultdict(
            lambda: 'fa-file-o',
            {x.mime_type: x.icon
             for x in IconMapping.objects.all()})
        object_list = []
        for x in os.listdir(self.path):
            mime_type = magic.from_file(
                '%s/%s' % (self.path, x), mime=True).decode('utf8')
            object_list.append({
                'name': x,
                'full_path': os.path.join(self.path, x),
                'directory': True if mime_type == 'inode/directory' else False,
                'mime_type': mime_type,
                'modified': datetime.fromtimestamp(
                    os.stat('%s/%s' % (self.path, x)).st_mtime),
                'size': os.stat('%s/%s' % (self.path, x)).st_size,
                'icon': icon_mapping[mime_type],
            })
        object_list.sort(key=lambda k: (not k['directory'], k['name']))
        dirs = filter(None, self.path.split(os.path.sep))
        path = [{
            'path': os.path.normpath('/'.join(dirs[:dirs.index(x) + 1])),
            'name': x
        } for x in dirs]
        up_one = None
        if self.path != self.fs.mountpoint:
            up_one = os.path.dirname(self.path)
        context.update({
            'up_one': up_one,
            'object_list': object_list,
            'path': path
        })
        return context


class FilesystemList(JSONResponseMixin, AjaxResponseMixin, BaseView, ListView):
    model = Filesystem
    headline = u'ZFS Filesystems'

    def get_ajax(self, request, *args, **kwargs):
        filesystems = []
        for fs in self.get_queryset().all():
            json_dict = get_status_dict(fs)
            json_dict['id'] = fs.id
            filesystems.append(json_dict)
        return self.render_json_response({'filesystems': filesystems})


class FilesystemDetail(JSONResponseMixin, AjaxResponseMixin, MessageMixin,
                       BaseView, DetailView):
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
            if (status is None
                    or status.state in states.READY_STATES
                    or status.state is None):
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


class FilesystemCreate(MessageMixin, BaseView, CreateView):
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


class FilesystemDelete(BaseView, DeleteView):
    model = Filesystem
    success_url = reverse_lazy(u'wizfs:filesystems')

    def get_headline(self):
        return u'Delete %s filesystem?' % self.get_object().name


class FilesystemUpdate(BaseView, UpdateView):
    model = Filesystem
    success_url = reverse_lazy(u'wizfs:filesystems')
    form_class = FilesystemForm

    def get_headline(self):
        return u'Edit %s filesystem' % self.get_object().name


class SnapshotSearchView(BaseView, FacetedSearchView):
    template = u'search.html'
    form_class = CrispyFacetedSearchForm
    results = None

    def get_headline(self):
        if self.search_field in self.request.REQUEST:
            return u'Search results'
        return u'Search'

    def get_form_kwargs(self):
        sqs = SearchQuerySet().facet(u'directory')
        kwargs = super(SnapshotSearchView, self).get_form_kwargs()
        kwargs.update({u'searchqueryset': sqs, u'data': self.request.REQUEST})
        return kwargs

    def form_valid(self, form):
        self.results = form.search()
        return super(SnapshotSearchView, self).form_valid(form)

    def form_invalid(self, form):
        self.results = form.search()
        return super(SnapshotSearchView, self).form_invalid(form)
