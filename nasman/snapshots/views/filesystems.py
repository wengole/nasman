from collections import defaultdict
from datetime import datetime
import logging
from pathlib import Path

from django.core.urlresolvers import reverse_lazy
import magic
from vanilla import TemplateView, FormView

from ..models import IconMapping
from ..forms import FileBrowserForm
from ..utils.zfs import ZFSUtil
from ..views.base import BaseView

logger = logging.getLogger(__name__)


class FileBrowser(BaseView, FormView):
    """
    Browse live filesystem using python os stdlib
    """
    template_name = 'file_list.html'
    headline = 'File Browser'
    form_class = FileBrowserForm
    success_url = reverse_lazy('nasman:file-browser')

    def get_context_data(self, **kwargs):
        """
        Build the context data for the file browser
        """
        context = super(FileBrowser, self).get_context_data(**kwargs)
        form = context['form']
        filesystem = None
        snapshot = None
        if form.is_bound:
            form.is_valid()
            filesystem = form.cleaned_data.get('filesystem')
            snapshot = form.cleaned_data.get('snapshot')
        if 'path' in form.changed_data:
            path = form.cleaned_data['path']
        elif 'filesystem' in form.changed_data:
            filesystem.mount()
            path = Path(filesystem.mountpoint)
        elif 'snapshot' in form.changed_data:
            snapshot.mount()
            path = Path(snapshot.mountpoint)
        else:
            path = Path('/')
        root = path.root
        icon_mapping = defaultdict(
            lambda: 'fa-file-o',
            {x.mime_type: x.icon
             for x in IconMapping.objects.all()})

        # The file list/browser
        object_list = []
        for x in path.iterdir():
            try:
                mime_type = magic.from_file(str(x), mime=True).decode('utf8')
            except OSError as e:
                logger.warn('Unable to get mime_type of %s', str(x))
                mime_type = None
            object_list.append({
                'name': x.name,
                'full_path': x,
                'directory': x.is_dir(),
                'mime_type': mime_type,
                'modified': datetime.fromtimestamp(x.lstat().st_mtime),
                'size': x.lstat().st_size,
                'icon': icon_mapping[mime_type],
            })
        object_list.sort(key=lambda k: (not k['directory'], k['name']))

        # Path breadcrumbs
        breadcrumbs = sorted(path.parents) + [path]

        # The up one '..' link
        up_one = None
        if path != root:
            up_one = path.parent

        # TODO: context relevant snapshot list
        context.update({
            'up_one': up_one,
            'object_list': object_list,
            'path': breadcrumbs,
            'browser_title': breadcrumbs[-1],
        })
        return context

    def form_valid(self, form):
        return self.form_invalid(form)


class FilesystemList(BaseView, TemplateView):
    template_name = 'filesystem_list.html'
    headline = 'ZFS Filesystems'

    def get_context_data(self, **kwargs):
        context = super(FilesystemList, self).get_context_data()
        context['object_list'] = ZFSUtil.get_filesystems()
        return context
