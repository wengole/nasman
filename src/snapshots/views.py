from haystack.generic_views import FacetedSearchView
from haystack.query import EmptySearchQuerySet


class SnapshotSearch(FacetedSearchView):
    """
    Search view for the Snapshot app
    """
    results = EmptySearchQuerySet()
    queryset = results

    def get_form_kwargs(self):
        kwargs = super(SnapshotSearch, self).get_form_kwargs()
        kwargs.update({'data': self.request.REQUEST})
        return kwargs

    def get_context_data(self, **kwargs):
        self.results = self.get_queryset()
        context = super(SnapshotSearch, self).get_context_data(**kwargs)
        context.update({
            'title': 'Search',
        })
        return context