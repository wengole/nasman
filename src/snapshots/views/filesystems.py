from collections import defaultdict
from datetime import datetime
import os

from braces.views import JSONResponseMixin, AjaxResponseMixin, MessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
import magic
from vanilla import TemplateView, ListView, DetailView, CreateView, DeleteView
from vanilla import UpdateView

from ..forms import FilesystemForm
from ..models import Filesystem, Snapshot, IconMapping
from ..utils import ZFSHelper
from ..views.base import BaseView


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


class FilesystemDetail(JSONResponseMixin, AjaxResponseMixin, MessageMixin,
                       BaseView, DetailView):
    model = Filesystem

    def get_headline(self):
        return u'%s Filesystem Details' % self.get_object().name


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
