# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0003_filesystem'),
    ]

    operations = [
        migrations.AddField(
            model_name='filesystem',
            name='mountpoint',
            field=models.CharField(max_length=255, verbose_name='mountpoint', blank=True),
            preserve_default=True,
        ),
    ]
