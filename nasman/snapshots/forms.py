import floppyforms as forms
from .utils.zfs import ZFSUtil


def filesystem_choices():
    filesystems = [x.name for x in ZFSUtil.get_filesystems()]
    choices = ((None, 'Select filesystem'),)
    return choices + tuple(zip(filesystems, filesystems))


class SmallSelectWidget(forms.Select):
    def get_context_data(self):
        context = super(SmallSelectWidget, self).get_context_data()
        context.update({
            'classes': ['input-sm']
        })
        return context

class SnapshotForm(forms.Form):
    name = forms.CharField(label='Snapshot name',
                           max_length=120,
                           required=True)
    filesystem = forms.TypedChoiceField(
        label='Parent filesystem',
        choices=filesystem_choices,
    )


class FileBrowserForm(forms.Form):
    filesystem = forms.ChoiceField(
        choices=filesystem_choices,
        widget=SmallSelectWidget
    )
