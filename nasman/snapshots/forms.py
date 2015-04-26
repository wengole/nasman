import floppyforms as forms

from .fields import FilesystemField, SnapshotField, PathField
from .widgets import SmallSelectWidget, BootstrapCheckboxWidget, BootstrapTextWidget, \
    BootstrapSelectWidget
from .utils.zfs import ZFSUtil


def filesystem_choices():
    """
    A callable for use by forms that allow choosing a ZFS Filesystem
    :return: The list of ZFS filesystems on the system
    :rtype: tuple
    """
    filesystems = [x.name for x in ZFSUtil.get_filesystems()]
    choices = (('placeholder', 'Select filesystem'),)
    return choices + tuple(zip(filesystems, filesystems))


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
