from braces.views import JSONResponseMixin, AjaxResponseMixin, SetHeadlineMixin
from vanilla import TemplateView

from ..mixins import SearchFormMixin


class BaseView(SetHeadlineMixin, SearchFormMixin):
    pass


class DashboardView(JSONResponseMixin, AjaxResponseMixin,
                    BaseView, TemplateView):
    """
    View for the homepage
    """
    http_method_names = [u'get']
    template_name = u'dashboard.html'
    headline = u'WiZFS Dashboard'
