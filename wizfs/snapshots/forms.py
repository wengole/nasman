from django import forms

from .models import Filesystem, Snapshot


class FilesystemForm(forms.ModelForm):

    class Meta:
        model = Filesystem
        fields = [u'name', u'mountpoint', u'parent']


class SnapshotForm(forms.ModelForm):

    class Meta:
        model = Snapshot
        fields = [u'name', u'filesystem']
