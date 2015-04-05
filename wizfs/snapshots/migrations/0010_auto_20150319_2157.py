# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0009_file_directory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filesystem',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='name'),
            preserve_default=True,
        ),
    ]
