# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fontawesome.fields


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0002_auto_20150428_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasmantreeitem',
            name='icon',
            field=fontawesome.fields.IconField(verbose_name='icon', blank=True, max_length=60, default='circle-o'),
        ),
    ]
