# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0007_file_magic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='created',
        ),
    ]
