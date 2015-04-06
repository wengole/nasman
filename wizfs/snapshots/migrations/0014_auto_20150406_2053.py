# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0013_auto_20150330_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iconmapping',
            name='icon',
            field=models.CharField(default=b'fa-file-o', max_length=25, verbose_name='icon', choices=[(b'fa-file-o', b'default'), (b'fa-file-archive-o', b'archive'), (b'fa-file-audio-o', b'audio'), (b'fa-file-code-o', b'code'), (b'fa-file-excel-o', b'excel'), (b'fa-file-image-o', b'image'), (b'fa-file-pdf-o', b'pdf'), (b'fa-file-powerpoint-o', b'powerpoint'), (b'fa-file-text-o', b'text'), (b'fa-file-video-o', b'video'), (b'fa-file-word-o', b'word'), (b'fa-folder-open-o', b'directory')]),
        ),
        migrations.AlterField(
            model_name='snapshot',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='snapshot',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='timestamp', null=True),
        ),
    ]
