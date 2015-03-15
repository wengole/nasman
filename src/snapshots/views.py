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
        paginator = context['paginator']
        page = context['page_obj']
        entries_from = (
            (
                (paginator.per_page * (page.number - 1)) + 1)
            if paginator.count > 0 else 0
        )
        entries_to = entries_from - 1 + paginator.per_page
        if paginator.count < entries_to:
            entries_to = paginator.count
        context.update({
            'title': 'Search',
            'item_numbers': '%s - %s' % (entries_from, entries_to),
        })
        return context