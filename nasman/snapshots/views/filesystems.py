from datetime import datetime

from collections import defaultdict
import os
import magic
from vanilla import TemplateView

from ..models import IconMapping
from ..utils import ZFSUtil, root_directory
from ..views.base import BaseView


class FileBrowser(BaseView, TemplateView):
    """
    Browse live filesystem using python os stdlib
    """
    template_name = 'file_list.html'
    headline = 'File Browser'
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
        dirs = list(filter(None, self.path.split(os.path.sep)))
        path = [{
            'path': os.path.normpath(
                os.path.join('/', *dirs[:dirs.index(x) + 1])
            ),
            'name': x
        } for x in dirs]
        path.insert(0, {
            'name': 'root',
            'path': root_directory()
        })
        up_one = None
        if self.path not in [self.fs.mountpoint, root_directory()]:
            up_one = os.path.dirname(self.path)
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
