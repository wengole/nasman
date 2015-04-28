import os
import yaml

PATH = os.path.join(os.path.dirname(__file__), 'icons.yml')
CHOICES = [('', '----------')]


def get_icon_choices():

    with open(PATH) as f:
        icons = yaml.load(f)

    for icon in icons.get('icons'):
        CHOICES.append((
            icon.get('id'),
            icon.get('name')
        ))

    return CHOICES
