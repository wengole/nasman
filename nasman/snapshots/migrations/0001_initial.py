# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.operations import HStoreExtension

from django.db import models, migrations
import djorm_pgfulltext.fields
import fontawesome.fields
import django.db.models.deletion
import sitetree.models
import nasman.snapshots.fields

import nasman.snapshots.models


class Migration(migrations.Migration):

    dependencies = [
        ('sitetree', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        HStoreExtension(),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('full_path', nasman.snapshots.fields.PathField(verbose_name='full path')),
                ('path_encoding', models.TextField(verbose_name='path encoding')),
                ('dirname', models.TextField(verbose_name='dirname', db_index=True)),
                ('name', models.TextField(verbose_name='name', db_index=True)),
                ('snapshot_name', models.TextField(verbose_name='snapshot', db_index=True)),
                ('directory', models.BooleanField(default=False)),
                ('magic', models.TextField(blank=True, verbose_name='magic')),
                ('modified', models.DateTimeField(verbose_name='modified')),
                ('size', models.IntegerField(null=True, blank=True, verbose_name='size')),
                ('search_index', djorm_pgfulltext.fields.VectorField(null=True, default='', db_index=True, editable=False, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='IconMapping',
            fields=[
                ('icon', models.CharField(default='fa-file-o', verbose_name='icon', choices=[('fa-file-o', 'default'), ('fa-file-archive-o', 'archive'), ('fa-file-audio-o', 'audio'), ('fa-file-code-o', 'code'), ('fa-file-excel-o', 'excel'), ('fa-file-image-o', 'image'), ('fa-file-pdf-o', 'pdf'), ('fa-file-powerpoint-o', 'powerpoint'), ('fa-file-text-o', 'text'), ('fa-file-video-o', 'video'), ('fa-file-word-o', 'word'), ('fa-folder-open-o', 'directory')], max_length=25)),
                ('mime_type', models.CharField(primary_key=True, verbose_name='mime-type', max_length=255, db_index=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='NasmanTreeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='Title', help_text='Site tree item title. Can contain template variables E.g.: {{ mytitle }}.', max_length=100)),
                ('hint', models.CharField(blank=True, default='', verbose_name='Hint', help_text='Some additional information about this item that is used as a hint.', max_length=200)),
                ('url', models.CharField(verbose_name='URL', db_index=True, help_text='Exact URL or URL pattern (see "Additional settings") for this item.', max_length=200)),
                ('urlaspattern', models.BooleanField(default=False, verbose_name='URL as Pattern', db_index=True, help_text='Whether the given URL should be treated as a pattern.<br /><b>Note:</b> Refer to Django "URL dispatcher" documentation (e.g. "Naming URL patterns" part).')),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden', db_index=True, help_text='Whether to show this item in navigation.')),
                ('alias', sitetree.models.CharFieldNullable(blank=True, db_index=True, null=True, verbose_name='Alias', help_text='Short name to address site tree item from a template.<br /><b>Reserved aliases:</b> "trunk", "this-children", "this-siblings", "this-ancestor-children", "this-parent-siblings".', max_length=80)),
                ('description', models.TextField(blank=True, default='', verbose_name='Description', help_text='Additional comments on this item.')),
                ('inmenu', models.BooleanField(default=True, verbose_name='Show in menu', db_index=True, help_text='Whether to show this item in a menu.')),
                ('inbreadcrumbs', models.BooleanField(default=True, verbose_name='Show in breadcrumb path', db_index=True, help_text='Whether to show this item in a breadcrumb path.')),
                ('insitetree', models.BooleanField(default=True, verbose_name='Show in site tree', db_index=True, help_text='Whether to show this item in a site tree.')),
                ('access_loggedin', models.BooleanField(default=False, verbose_name='Logged in only', db_index=True, help_text='Check it to grant access to this item to authenticated users only.')),
                ('access_guest', models.BooleanField(default=False, verbose_name='Guests only', db_index=True, help_text='Check it to grant access to this item to guests only.')),
                ('access_restricted', models.BooleanField(default=False, verbose_name='Restrict access to permissions', db_index=True, help_text='Check it to restrict user access to this item, using Django permissions system.')),
                ('access_perm_type', models.IntegerField(default=1, verbose_name='Permissions interpretation', help_text='<b>Any</b> &mdash; user should have any of chosen permissions. <b>All</b> &mdash; user should have all chosen permissions.', choices=[(1, 'Any'), (2, 'All')])),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order', db_index=True, help_text='Item position among other site tree items under the same parent.')),
                ('icon', fontawesome.fields.IconField(blank=True, default='circle-o', verbose_name='icon', max_length=60)),
                ('access_permissions', models.ManyToManyField(blank=True, verbose_name='Permissions granting access', to='auth.Permission')),
                ('parent', models.ForeignKey(blank=True, related_name='nasmantreeitem_parent', to='snapshots.NasmanTreeItem', null=True, verbose_name='Parent', help_text='Parent site tree item.')),
                ('tree', models.ForeignKey(related_name='nasmantreeitem_tree', to='sitetree.Tree', verbose_name='Site Tree', help_text='Site tree this item belongs to.')),
            ],
            options={
                'verbose_name': 'Site Tree Item',
                'abstract': False,
                'verbose_name_plural': 'Site Tree Items',
            },
        ),
        migrations.AddField(
            model_name='file',
            name='mime_type',
            field=models.ForeignKey(null=True, verbose_name='mime-type', on_delete=django.db.models.deletion.SET_NULL, to='snapshots.IconMapping'),
        ),
        migrations.AlterUniqueTogether(
            name='nasmantreeitem',
            unique_together=set([('tree', 'alias')]),
        ),
    ]
