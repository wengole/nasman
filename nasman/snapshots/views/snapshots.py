from braces.views import MessageMixin
from django.shortcuts import redirect
from django.views.generic import View
from vanilla import FormView, TemplateView

from ..forms import SnapshotForm
from .base import BaseView
from nasman.snapshots import tasks
from ..utils import ZFSUtil


class SnapshotCreate(MessageMixin, BaseView, FormView):
    headline = 'Create new snapshot'
    form_class = SnapshotForm
    template_name = 'snapshot_form.html'


class SnapshotList(BaseView, TemplateView):
    headline = 'ZFS Snapshots'
    template_name = 'snapshot_list.html'

    def get_context_data(self, **kwargs):
        context = super(SnapshotList, self).get_context_data()
        context['object_list'] = ZFSUtil.get_snapshots()
        return context


class SnapshotReindex(View):
    http_method_names = ['get']

    def get(self, request, name=None):
        snap = ZFSUtil.get_snapshot(name)
        res = tasks.walk_and_reindex.delay(
            path='%s/.zfs/snapshot/%s' % (snap.mountpoint, snap.basename)
        )
        return redirect('nasman:snapshots')
