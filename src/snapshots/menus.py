from django.core.urlresolvers import reverse

from menu import MenuItem
from menu import Menu


def snapshots_menu(request):
    menu = [
        MenuItem(
            title='Snapshots',
            url='#',
            classes='dropdown-header'
        ),
        MenuItem(
            title='List Snapshots',
            url=reverse('snapshots:list'),
        ),
    ]
    return menu


Menu.add_item(
    'top_nav_left',
    MenuItem(
        title='Snapshots',
        url='#',
        children=snapshots_menu,
        classes='dropdown',
        #TODO: Restrict showing menu
        # check=lambda x: True
    )
)