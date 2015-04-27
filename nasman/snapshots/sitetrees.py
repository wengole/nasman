from sitetree.utils import tree, item


sitetrees = (
    tree(
        'sidebar',
        title='NAVIGATION',
        items=(
            item(
                'File Browser',
                'nasman:file-browser'
            ),
            item(
                'List Filesystems',
                'nasman:filesystems'
            ),
            item(
                'List Snapshots',
                'nasman:snapshots'
            ),
        )),
)
