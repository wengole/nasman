# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0002_auto_20150223_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filesystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('parent', models.ForeignKey(blank=True, to='snapshots.Filesystem', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
