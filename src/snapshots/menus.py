from django.core.urlresolvers import reverse

from menu import MenuItem
from menu import Menu


def snapshots_menu(request):
    menu = [
        MenuItem(
            title='File Browser',
            url=reverse('wizfs:file-browser'),
        ),
        MenuItem(
            title='Filesystems',
            url=reverse('wizfs:filesystems')
        )
    ]
    return menu


Menu.add_item(
    'top_nav_left',
    MenuItem(
        title='File',
        url='#',
        children=snapshots_menu,
        classes='dropdown',
        #TODO: Restrict showing menu
        # check=lambda x: True
    )
)