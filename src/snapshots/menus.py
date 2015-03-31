from django.core.urlresolvers import reverse

from menu import MenuItem
from menu import Menu


def snapshots_menu(request):
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
        title=u'File',
        url=u'#',
        children=snapshots_menu,
        classes=u'dropdown',
        #TODO: Restrict showing menu
        # check=lambda x: True
    )
)
