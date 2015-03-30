# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0012_file_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='IconMapping',
            fields=[
                ('icon', models.CharField(default=b'fa-file-o', max_length=25, verbose_name='icon', choices=[(b'fa-file-o', b'default'), (b'fa-file-archive-o', b'archive'), (b'fa-file-audio-o', b'audio'), (b'fa-file-code-o', b'code'), (b'fa-file-excel-o', b'excel'), (b'fa-file-image-o', b'image'), (b'fa-file-pdf-o', b'pdf'), (b'fa-file-powerpoint-o', b'powerpoint'), (b'fa-file-text-o', b'text'), (b'fa-file-video-o', b'video'), (b'fa-file-word-o', b'word')])),
                ('mime_type', models.CharField(max_length=255, serialize=False, verbose_name='mime-type', primary_key=True, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='file',
            name='mime_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='mime-type', to='snapshots.IconMapping', null=True),
            preserve_default=True,
        ),
    ]
