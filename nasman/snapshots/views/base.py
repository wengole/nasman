from braces.views import SetHeadlineMixin
from vanilla import TemplateView


class BaseView(SetHeadlineMixin):
    pass


class DashboardView(BaseView,
                    TemplateView):
    """
    View for the homepage
    """
    http_method_names = ['get']
    template_name = 'dashboard.html'
    headline = 'NASMan Dashboard'
