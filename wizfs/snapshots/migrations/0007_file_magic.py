# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0006_remove_file_extension'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='magic',
            field=models.CharField(max_length=255, verbose_name='magic', blank=True),
            preserve_default=True,
        ),
    ]
