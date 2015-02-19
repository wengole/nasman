from django import forms
from snapshots.models import Snapshot, File


class SnapshotForm(forms.ModelForm):

    class Meta:
        model = Snapshot
        fields = ['name', 'timestamp']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(SnapshotForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(SnapshotForm, self).is_valid()

    def full_clean(self):
        return super(SnapshotForm, self).full_clean()

    def clean_name(self):
        name = self.cleaned_data.get("name", None)
        return name

    def clean_timestamp(self):
        timestamp = self.cleaned_data.get("timestamp", None)
        return timestamp

    def clean(self):
        return super(SnapshotForm, self).clean()

    def validate_unique(self):
        return super(SnapshotForm, self).validate_unique()

    def save(self, commit=True):
        return super(SnapshotForm, self).save(commit)


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['full_path', 'snapshot', 'mime_type', 'extension', 'created', 'modified', 'size']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(FileForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(FileForm, self).is_valid()

    def full_clean(self):
        return super(FileForm, self).full_clean()

    def clean_full_path(self):
        full_path = self.cleaned_data.get("full_path", None)
        return full_path

    def clean_snapshot(self):
        snapshot = self.cleaned_data.get("snapshot", None)
        return snapshot

    def clean_mime_type(self):
        mime_type = self.cleaned_data.get("mime_type", None)
        return mime_type

    def clean_extension(self):
        extension = self.cleaned_data.get("extension", None)
        return extension

    def clean_created(self):
        created = self.cleaned_data.get("created", None)
        return created

    def clean_modified(self):
        modified = self.cleaned_data.get("modified", None)
        return modified

    def clean_size(self):
        size = self.cleaned_data.get("size", None)
        return size

    def clean(self):
        return super(FileForm, self).clean()

    def validate_unique(self):
        return super(FileForm, self).validate_unique()

    def save(self, commit=True):
        return super(FileForm, self).save(commit)
