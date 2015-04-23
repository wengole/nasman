from datetime import datetime

from collections import defaultdict
import magic
from pathlib import Path
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
    fs = None
    path = None
    snapshot = None

    def get(self, request, *args, **kwargs):
        fs_name = self.request.GET.get('fs')
        self.path = self.request.GET.get('path')
        if fs_name is not None:
            self.fs = ZFSUtil.get_filesystem(fs_name)
        else:
            self.fs = ZFSUtil.get_filesystems()[0]
        return super(FileBrowser, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Build the context data for the file browser
        """
        context = super(FileBrowser, self).get_context_data(**kwargs)
        if self.path is None:
            self.path = Path(self.fs.mountpoint).root
        self.path = Path(self.path)
        icon_mapping = defaultdict(
            lambda: 'fa-file-o',
            {x.mime_type: x.icon
             for x in IconMapping.objects.all()})
        object_list = []
        for x in self.path.iterdir():
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
        path = sorted(self.path.parents) + [self.path]
        up_one = None
        if self.path not in [self.fs.mountpoint, self.path.root]:
            up_one = self.path.parent
        context.update({
            'up_one': up_one,
            'object_list': object_list,
            'path': path
        })
        return context


class FilesystemList(BaseView, TemplateView):
    template_name = 'filesystem_list.html'
    headline = 'ZFS Filesystems'

    def get_context_data(self, **kwargs):
        context = super(FilesystemList, self).get_context_data()
        context['object_list'] = ZFSUtil.get_filesystems()
        return context
