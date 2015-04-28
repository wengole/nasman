from sitetree.utils import tree, item


sitetrees = (
    tree(
        'sidebar',
        title='NAVIGATION',
        items=(
            item(
                'File Browser',
                'nasman:file-browser',
                icon='search',
            ),
            item(
                'List Filesystems',
                'nasman:filesystems',
                icon='files-o',
            ),
            item(
                'List Snapshots',
                'nasman:snapshots',
                icon='camera',
            ),
        )),
)
