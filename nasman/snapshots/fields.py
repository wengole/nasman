from pathlib import Path
import floppyforms as forms
from nasman.snapshots.utils.zfs import ZFSUtil


class FilesystemField(forms.ChoiceField):
    def clean(self, value):
        if value:
            return ZFSUtil.get_filesystem(value)


class SnapshotField(forms.ChoiceField):
    def clean(self, value):
        if value:
            return ZFSUtil.get_snapshot(value)


class PathField(forms.Field):
    def clean(self, value):
        if value:
            return Path(value)
