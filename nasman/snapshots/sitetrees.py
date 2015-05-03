from sitetree.utils import tree, item


sitetrees = (
    tree(
        'sidebar',
        title='NAVIGATION',
        items=(
            item(
                'Dashboard',
                'nasman:dashboard',
                icon='dashboard',
            ),
            item(
                'Filebrowser',
                'nasman:file-browser',
                icon='search',
            ),
        )),
)
