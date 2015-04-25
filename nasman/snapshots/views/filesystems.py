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

    def get_context_data(self, **kwargs):
        """
        Build the context data for the file browser
        """
        context = super(FileBrowser, self).get_context_data(**kwargs)
        form = context['form']
        if form.is_bound:
            form.is_valid()
            # filesystem = form.cleaned_data.get('filesystem')
            # snapshot = form.cleaned_data.get('snapshot')
        if 'path' in form.changed_data:
            path = form.cleaned_data['path']
        elif 'filesystem' in form.changed_data:
            path = Path(form.cleaned_data['filesystem'].mountpoint)
        elif 'snapshot' in form.changed_data:
            snapshot = form.cleaned_data['snapshot']
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
        extra_sidebar = {
            'id': 'snapshot-list',
            'header': 'Snapshots',
            'list': [
                {'link': x.name,
                 'title': x.name} for x in ZFSUtil.get_snapshots()
            ]
        }
        context.update({
            'up_one': up_one,
            'object_list': object_list,
            'path': breadcrumbs,
            'extra_sidebar': extra_sidebar,
            # 'filesystem': filesystem,
            # 'snapshot': snapshot
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
