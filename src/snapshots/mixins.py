from snapshots.forms import CrispyFacetedSearchForm


class SearchFormMixin(object):
    """
    Mixin to add search form to any view
    """
    def get_context_data(self, **kwargs):
        form = CrispyFacetedSearchForm()
        return super(SearchFormMixin, self).get_context_data(
            search_form=form, **kwargs)
