from django.core.urlresolvers import reverse

from menu import MenuItem
from menu import Menu


def filesystems_menu(request):
    menu = [
        MenuItem(
            title=u'File Browser',
            url=reverse(u'wizfs:file-browser'),
        ),
        MenuItem(
            title=u'Filesystems',
            url=reverse(u'wizfs:filesystems')
        )
    ]
    return menu


Menu.add_item(
    u'top_nav_left',
    MenuItem(
        title=u'Files',
        url=u'#',
        children=filesystems_menu,
        classes=u'dropdown',
        #TODO: Restrict showing menu
        # check=lambda x: True
    )
)


def snapshots_menu(request):
    menu = [
        MenuItem(
            title=u'Snapshots',
            url=reverse(u'wizfs:snapshots')
        )
    ]
    return menu


Menu.add_item(
    u'top_nav_left',
    MenuItem(
        title=u'Snapshots',
        url=u'#',
        children=snapshots_menu,
        classes=u'dropdown'
    )
)
