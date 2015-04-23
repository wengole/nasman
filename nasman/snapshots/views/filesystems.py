from datetime import datetime
from pathlib import Path

from collections import defaultdict
from django.core.urlresolvers import reverse_lazy
import magic
from vanilla import TemplateView, FormView

from ..models import IconMapping
from ..forms import FileBrowserForm
from ..utils.zfs import ZFSUtil
from ..views.base import BaseView


class FileBrowser(BaseView, FormView):
    """
    Browse live filesystem using python os stdlib
    """
    template_name = 'file_list.html'
    headline = 'File Browser'
    form_class = FileBrowserForm
    success_url = reverse_lazy('nasman:file-browser')

    def get_form(self, data=None, files=None, **kwargs):
        if data is None:
            data = {
                'path': '/'
            }
        else:
            path = data.get('path')
            if path is None:
                fs = data.get('filesystem')
                snap = data.get('snapshot')
                data.update({
                    'path': fs.mountpoint or snap.mountpoint
                })
        form = self.get_form_class()(data)
        form.is_valid()
        return form

    def get_context_data(self, **kwargs):
        """
        Build the context data for the file browser
        """
        context = super(FileBrowser, self).get_context_data(**kwargs)
        form = context['form']
        path = form.cleaned_data.get('path') or Path('/')
        fs = form.cleaned_data.get('filesystem')
        root = Path(path.root)
        if fs is not None:
            root = path = Path(fs.mountpoint)
        icon_mapping = defaultdict(
            lambda: 'fa-file-o',
            {x.mime_type: x.icon
             for x in IconMapping.objects.all()})

        # The file list/browser
        object_list = []
        for x in path.iterdir():
            mime_type = magic.from_file(str(x), mime=True).decode('utf8')
            object_list.append({
                'name': x.name,
                'full_path': x,
                'directory': x.is_dir(),
                'mime_type': mime_type,
                'modified': datetime.fromtimestamp(x.stat().st_mtime),
                'size': x.stat().st_size,
                'icon': icon_mapping[mime_type],
            })
        object_list.sort(key=lambda k: (not k['directory'], k['name']))

        # Path breadcrumbs
        breadcrumbs = sorted(path.parents) + [path]

        # The up one '..' link
        up_one = None
        if path != root:
            up_one = path.parent

        # Snapshot list for sidebar

        context.update({
            'up_one': up_one,
            'object_list': object_list,
            'path': breadcrumbs
        })
        return context

    def form_valid(self, form):
        pass


class FilesystemList(BaseView, TemplateView):
    template_name = 'filesystem_list.html'
    headline = 'ZFS Filesystems'

    def get_context_data(self, **kwargs):
        context = super(FilesystemList, self).get_context_data()
        context['object_list'] = ZFSUtil.get_filesystems()
        return context
