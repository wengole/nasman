from haystack.generic_views import FacetedSearchView
from haystack.query import SearchQuerySet

from ..forms import CrispyFacetedSearchForm
from ..views.base import BaseView

__author__ = 'benc'


class SnapshotSearchView(BaseView, FacetedSearchView):
    template = u'search.html'
    form_class = CrispyFacetedSearchForm
    results = None

    def get_headline(self):
        if self.search_field in self.request.REQUEST:
            return u'Search results'
        return u'Search'

    def get_form_kwargs(self):
        sqs = SearchQuerySet().facet(u'directory')
        kwargs = super(SnapshotSearchView, self).get_form_kwargs()
        kwargs.update({u'searchqueryset': sqs, u'data': self.request.REQUEST})
        return kwargs

    def form_valid(self, form):
        self.results = form.search()
        return super(SnapshotSearchView, self).form_valid(form)

    def form_invalid(self, form):
        self.results = form.search()
        return super(SnapshotSearchView, self).form_invalid(form)
