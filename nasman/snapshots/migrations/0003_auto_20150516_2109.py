# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fontawesome.fields


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0002_zfsfilesystem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZFSSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.TextField(help_text='Unique name of this snapshot', verbose_name='name', unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='iconmapping',
            name='icon',
            field=fontawesome.fields.IconField(max_length=60, help_text='The FontAwesome icon for this mime type', default='fa-file-o', verbose_name='icon', blank=True),
        ),
        migrations.AlterField(
            model_name='iconmapping',
            name='mime_type',
            field=models.CharField(help_text='The mime type', db_index=True, verbose_name='mime-type', max_length=255, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='zfsfilesystem',
            name='mountpoint',
            field=models.TextField(help_text='The set mountpoint of the filesystem', verbose_name='mountpoint'),
        ),
        migrations.AlterField(
            model_name='zfsfilesystem',
            name='name',
            field=models.TextField(help_text='Unique name of this filesystem', verbose_name='name', unique=True),
        ),
    ]
