from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    View for the homepage
    """
    http_method_names = [u'get']
    template_name = 'dashboard.html'
