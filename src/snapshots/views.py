"""
Snapshot app views
"""
from django.views.generic import TemplateView, ListView
from snapshots.models import File


class DashboardView(TemplateView):
    """
    View for the homepage
    """
    http_method_names = [u'get']
    template_name = 'dashboard.html'


class FileBrowser(ListView):
    model = File