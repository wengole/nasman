from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.urlresolvers import reverse
from haystack.forms import FacetedSearchForm

from .models import Filesystem


class FilesystemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FilesystemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Filesystem
        fields = ['name', 'mountpoint', 'parent']


class CrispyFacetedSearchForm(FacetedSearchForm):
    def __init__(self, *args, **kwargs):
        super(CrispyFacetedSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = u'GET'
        self.helper.form_action = reverse('wizfs:search')
        self.helper.layout.append(Submit(u'search', u'search'))
        self.helper.form_class = u'navbar-form navbar-right'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
