from pathlib import Path

import floppyforms as forms

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


class SmallSelectWidget(forms.Select):
    def get_context_data(self):
        context = super(SmallSelectWidget, self).get_context_data()
        context.update({
            'classes': ['input-sm']
        })
        return context


class FilesystemField(forms.ChoiceField):
    def clean(self, value):
        if value is not None:
            return ZFSUtil.get_filesystem(value)


class SnapshotField(forms.ChoiceField):
    def clean(self, value):
        if value is not None:
            return ZFSUtil.get_snapshot(value)


class PathField(forms.Field):
    def clean(self, value):
        if value is not None:
            return Path(value)


class SnapshotForm(forms.Form):
    name = forms.CharField(
        label='Snapshot name',
        max_length=120,
        required=True
    )
    filesystem = forms.TypedChoiceField(
        label='Parent filesystem',
        choices=filesystem_choices,
    )


class FileBrowserForm(forms.Form):
    filesystem = FilesystemField(
        choices=filesystem_choices,
        widget=SmallSelectWidget
    )
    snapshot = SnapshotField(widget=forms.HiddenInput)
    path = PathField(widget=forms.HiddenInput)
