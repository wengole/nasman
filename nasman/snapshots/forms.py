import floppyforms as forms
from nasman.snapshots.utils import ZFSUtil


def filesystem_choices():
    filesystems = [x.name for x in ZFSUtil.get_filesystems()]
    choices = ((None, '-'),)
    return choices + tuple(zip(filesystems, filesystems))


class SnapshotForm(forms.Form):
    name = forms.CharField(label='Snapshot name',
                           max_length=120,
                           required=True)
    filesystem = forms.TypedChoiceField(
        label='Parent filesystem',
        choices=filesystem_choices,
    )
