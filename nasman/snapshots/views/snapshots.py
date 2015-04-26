from braces.views import MessageMixin
from django.shortcuts import redirect
from django.views.generic import View
from vanilla import FormView, TemplateView

from ..forms import SnapshotForm
from .base import BaseView
from nasman.snapshots import tasks
from ..utils.zfs import ZFSUtil


class SnapshotCreate(MessageMixin, BaseView, FormView):
    headline = 'Create new snapshot'
    form_class = SnapshotForm
    template_name = 'snapshot_form.html'

    def form_valid(self, form):
        pass


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


class SnapshotMount(MessageMixin, View):
    http_method_names = ['get']

    def get(self, request, name=None):
        snap = ZFSUtil.get_snapshot(name)
        if snap.is_mounted:
            if snap.unmount():
                self.messages.info('{0} is now unmounted'.format(name))
            else:
                self.messages.error('Failed to unmount {0}'.format(name))
        else:
            if snap.mount():
                self.messages.info('{0} is now mounted at {1}'.format(
                    name, snap.mountpoint))
        return redirect('nasman:snapshots')
