from pathlib import Path
import floppyforms as forms

from nasman.snapshots.utils.zfs import ZFSUtil
from .utils.zfs import ZFSUtil
from .widgets import (
    SmallSelectWidget,
    BootstrapCheckboxWidget,
    BootstrapTextWidget,
    BootstrapSelectWidget
)


def filesystem_choices():
    """
    A callable for use by forms that allow choosing a ZFS Filesystem
    :return: The list of ZFS filesystems on the system
    :rtype: tuple
    """
    filesystems = [x.name for x in ZFSUtil.get_filesystems()]
    choices = (('placeholder', 'Select filesystem'),)
    return choices + tuple(zip(filesystems, filesystems))


class PathField(forms.Field):
    def clean(self, value):
        if value:
            return Path(value)


class FilesystemField(forms.ChoiceField):
    def clean(self, value):
        if value:
            return ZFSUtil.get_filesystem(value)


class SnapshotField(forms.ChoiceField):
    def clean(self, value):
        if value:
            return ZFSUtil.get_snapshot(value)


class SnapshotForm(forms.Form):
    name = forms.CharField(
        label='Snapshot name',
        max_length=120,
        required=True,
        widget=BootstrapTextWidget,
    )
    filesystem = forms.TypedChoiceField(
        label='Parent filesystem',
        choices=filesystem_choices,
        widget=BootstrapSelectWidget,
    )
    recursive = forms.BooleanField(
        label='Recurse filesystems?',
        widget=BootstrapCheckboxWidget,
        required=False,
    )


class FileBrowserForm(forms.Form):
    filesystem = FilesystemField(
        choices=filesystem_choices,
        widget=SmallSelectWidget()
    )
    snapshot = SnapshotField(widget=forms.HiddenInput)
    path = PathField(widget=forms.HiddenInput)
