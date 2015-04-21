# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgfulltext.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('full_path', models.TextField(verbose_name='full path')),
                ('dirname', models.TextField(verbose_name='dirname', db_index=True)),
                ('name', models.TextField(verbose_name='name', db_index=True)),
                ('snapshot_name', models.TextField(verbose_name='snapshot', db_index=True)),
                ('directory', models.BooleanField(default=False)),
                ('magic', models.CharField(verbose_name='magic', blank=True, max_length=255)),
                ('modified', models.DateTimeField(verbose_name='modified')),
                ('size', models.IntegerField(verbose_name='size', blank=True, null=True)),
                ('search_index', djorm_pgfulltext.fields.VectorField(default='', db_index=True, null=True, editable=False, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='IconMapping',
            fields=[
                ('icon', models.CharField(default='fa-file-o', choices=[('fa-file-o', 'default'), ('fa-file-archive-o', 'archive'), ('fa-file-audio-o', 'audio'), ('fa-file-code-o', 'code'), ('fa-file-excel-o', 'excel'), ('fa-file-image-o', 'image'), ('fa-file-pdf-o', 'pdf'), ('fa-file-powerpoint-o', 'powerpoint'), ('fa-file-text-o', 'text'), ('fa-file-video-o', 'video'), ('fa-file-word-o', 'word'), ('fa-folder-open-o', 'directory')], max_length=25, verbose_name='icon')),
                ('mime_type', models.CharField(verbose_name='mime-type', db_index=True, primary_key=True, max_length=255, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='mime_type',
            field=models.ForeignKey(to='snapshots.IconMapping', null=True, verbose_name='mime-type', on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
