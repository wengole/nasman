# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0008_remove_file_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='directory',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
