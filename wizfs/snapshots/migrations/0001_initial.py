# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_path', models.CharField(max_length=255, verbose_name=b'full path')),
                ('mime_type', models.CharField(max_length=255, verbose_name=b'mime type', blank=True)),
                ('extension', models.CharField(max_length=255, verbose_name=b'extension', blank=True)),
                ('created', models.DateTimeField(verbose_name=b'created')),
                ('modified', models.DateTimeField(verbose_name=b'modified')),
                ('size', models.IntegerField(null=True, verbose_name=b'size', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'name')),
                ('timestamp', models.DateTimeField(verbose_name=b'timestamp')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='file',
            name='snapshot',
            field=models.ForeignKey(verbose_name=b'snapshot', blank=True, to='snapshots.Snapshot', null=True),
            preserve_default=True,
        ),
    ]
