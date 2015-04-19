from sitetree.utils import tree, item


sitetrees = (
    tree(
        'sidebar',
        title='NAVIGATION',
        items=(
            item(
                'Files',
                '#',
                children=[
                    item(
                        'File Browser',
                        'nasman:file-browser'
                    ),
                    item(
                        'List Filesystems',
                        'nasman:filesystems'
                    )
                ]
            ),
            item(
                'Snapshots',
                '#',
                children=[
                    item(
                        'List Snapshots',
                        'nasman:snapshots'
                    )
                ]
            ),
        )),
)
