from braces.views import MessageMixin, JSONResponseMixin, AjaxResponseMixin
from django.shortcuts import redirect
from vanilla import CreateView, ListView

from ..forms import SnapshotForm
from ..models import Snapshot
from ..utils import ZFSHelper
from ..views.base import BaseView


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
