# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snapshot',
            name='timestamp',
            field=models.DateTimeField(null=True, verbose_name=b'timestamp', blank=True),
            preserve_default=True,
        ),
    ]
