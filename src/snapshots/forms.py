from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.urlresolvers import reverse
from haystack.forms import FacetedSearchForm

from .models import Filesystem, Snapshot


class FilesystemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FilesystemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit(u'save', u'save'))

    class Meta:
        model = Filesystem
        fields = [u'name', u'mountpoint', u'parent']


class CrispyFacetedSearchForm(FacetedSearchForm):
    def __init__(self, *args, **kwargs):
        super(CrispyFacetedSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = u'GET'
        self.helper.form_action = reverse(u'wizfs:search')
        self.helper.layout.append(Submit(u'search', u'search'))
        self.helper.form_class = u'navbar-form navbar-right'
        self.helper.field_template = u'bootstrap3/layout/inline_field.html'


class SnapshotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SnapshotForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit(u'save', u'save'))

    class Meta:
        model = Snapshot
        fields = [u'name', u'filesystem']
