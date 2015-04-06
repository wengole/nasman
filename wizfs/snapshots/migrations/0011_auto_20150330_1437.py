# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0010_auto_20150319_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='dirname',
            field=models.TextField(default='', verbose_name='dirname', db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='file',
            name='full_path',
            field=models.TextField(verbose_name='full path'),
            preserve_default=True,
        ),
    ]
