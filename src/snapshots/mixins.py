from snapshots.forms import CrispyFacetedSearchForm


class SearchFormMixin(object):
    """
    Mixin to add search form to any view
    """
    def get_context_data(self, **kwargs):
        form_class = getattr(self, 'form_class', None)
        if form_class is None:
            form_class = CrispyFacetedSearchForm
        form = form_class()

        return super(SearchFormMixin, self).get_context_data(
            search_form=form, **kwargs)

