# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0004_filesystem_mountpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='snapshot',
            name='filesystem',
            field=models.ForeignKey(related_name='snapshots', default=1, to='snapshots.Filesystem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filesystem',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='snapshots.Filesystem', null=True),
            preserve_default=True,
        ),
    ]
