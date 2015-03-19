"""
Snapshot app views
"""
from django.contrib import messages
from vanilla import TemplateView, ListView, DetailView, CreateView

from .models import File, Filesystem
from .tasks import reindex_filesystem


class DashboardView(TemplateView):
    """
    View for the homepage
    """
    http_method_names = [u'get']
    template_name = 'dashboard.html'


class FileBrowser(ListView):
    model = File


class FilesystemList(ListView):
    model = Filesystem


class FilesystemDetail(DetailView):
    model = Filesystem

    def get(self, request, *args, **kwargs):
        if request.GET.get('reindex'):
            self.object = self.get_object()
            context = self.get_context_data()
            fs = self.get_object()
            result = reindex_filesystem.delay(fs.name)
            messages.add_message(request,
                                 messages.INFO,
                                 'Reindex of %s started' % fs.name)
            return self.render_to_response(context)
        return super(FilesystemDetail, self).get(request, *args, **kwargs)


class FilesystemCreate(CreateView):
    model = Filesystem