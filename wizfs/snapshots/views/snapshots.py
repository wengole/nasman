from braces.views import MessageMixin, JSONResponseMixin, AjaxResponseMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from vanilla import (CreateView,
                     ListView,
                     UpdateView,
                     DetailView,
                     DeleteView)

from ..forms import SnapshotForm
from ..models import Snapshot
from ..utils import ZFSHelper
from .base import BaseView


class SnapshotCreate(MessageMixin, BaseView, CreateView):
    model = Snapshot
    headline = u'Add New Filesystem'
    form_class = SnapshotForm

    def get(self, request, *args, **kwargs):
        """
        If "auto" query parameter is passed then use utility to add all found
        filesystems
        """
        if request.GET.get(u'auto'):
            util = ZFSHelper()
            util.create_snapshot_objects()
            self.messages.info(u'Added all snapshots automatically')
            return redirect(u'wizfs:snapshots')
        return super(SnapshotCreate, self).get(request, *args, **kwargs)


class SnapshotList(JSONResponseMixin, AjaxResponseMixin, BaseView, ListView):
    model = Snapshot
    headline = u'ZFS Snapshots'


class SnapshotUpdate(BaseView, UpdateView):
    model = Snapshot
    success_url = reverse_lazy(u'wizfs:snapshots')
    form_class = SnapshotForm

    def get_headline(self):
        return u'Edit %s snapshot' % self.get_object().name


class SnapshotDetail(JSONResponseMixin,
                     AjaxResponseMixin,
                     MessageMixin,
                     BaseView,
                     DetailView):
    model = Snapshot

    def get_headline(self):
        return u'Snapshot %s Details' % self.get_object().name


class SnapshotDelete(BaseView, DeleteView):
    model = Snapshot
    success_url = reverse_lazy(u'wizfs:snapshots')

    def get_headline(self):
        return u'Delete snapshot: %s ?' % self.get_object().name
