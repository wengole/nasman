# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0011_auto_20150330_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.TextField(default='', verbose_name='name'),
            preserve_default=False,
        ),
    ]
