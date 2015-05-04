import logging
from subprocess import CalledProcessError

from braces.views import MessageMixin, JSONResponseMixin, AjaxResponseMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import View
from vanilla import FormView, ListView

from ..forms import SnapshotForm
from .base import BaseView
from .. import tasks
from ..utils.zfs import ZFSUtil


logger = logging.getLogger(__name__)


class SnapshotCreate(MessageMixin, BaseView, FormView):
    headline = 'Create new snapshot'
    form_class = SnapshotForm
    template_name = 'snapshot_form.html'
    success_url = reverse_lazy('nasman:snapshots')

    def form_valid(self, form):
        snap_name = form.cleaned_data['name']
        fs_name = form.cleaned_data['filesystem']
        recurse = form.cleaned_data['recursive']
        try:
            ZFSUtil.create_snapshot(snap_name, fs_name, recurse)
        except CalledProcessError as e:
            self.messages.error(
                '{1}'.format(
                    snap_name,
                    str(e.output.decode('utf-8'))
                ).capitalize(),
                extra_tags='ban'
            )
        else:
            self.messages.info(
                'Created {0}'.format(form.cleaned_data['name'])
            )
        return super(SnapshotCreate, self).form_valid(form)

class SnapshotList(JSONResponseMixin, AjaxResponseMixin, BaseView, ListView):
    headline = 'ZFS Snapshots'
    template_name = 'snapshot_list.html'
    refresh = False
    context_object_name = 'snapshot_list'

    def get_ajax(self, request, *args, **kwargs):
        draw = int(self.request.GET.get('draw')) + 1
        records = self.get_queryset()
        record_count = len(records)
        json_dict = {
            'draw': draw,
            'recordsTotal': record_count,
            'recordsFiltered': record_count,
            'data': records
        }
        return self.render_json_response(json_dict)

    def get_queryset(self):
        logger.info('Getting snapshot list refresh: %s', self.refresh)
        return ZFSUtil.get_snapshots(self.refresh)


class SnapshotReindex(MessageMixin, View):
    http_method_names = ['get']

    def get(self, request, name=None):
        res = tasks.index_snapshot.apply_async(args=(name, ))
        self.messages.info('Reindex of {0} started'.format(name))
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
