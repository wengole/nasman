from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from .models import Filesystem


class FilesystemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FilesystemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Filesystem
        fields = ['name', 'mountpoint', 'parent']
