# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sitetree.models
import nasman.snapshots.models
import fontawesome.fields
import djorm_pgfulltext.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('snapshots', '0001_initial'), ('snapshots', '0002_auto_20150428_1227'), ('snapshots', '0003_auto_20150428_1230')]

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('full_path', models.TextField(verbose_name='full path')),
                ('dirname', models.TextField(db_index=True, verbose_name='dirname')),
                ('name', models.TextField(db_index=True, verbose_name='name')),
                ('snapshot_name', models.TextField(db_index=True, verbose_name='snapshot')),
                ('directory', models.BooleanField(default=False)),
                ('magic', models.CharField(max_length=255, blank=True, verbose_name='magic')),
                ('modified', models.DateTimeField(verbose_name='modified')),
                ('size', models.IntegerField(blank=True, verbose_name='size', null=True)),
                ('search_index', djorm_pgfulltext.fields.VectorField(default='', serialize=False, editable=False, db_index=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IconMapping',
            fields=[
                ('icon', models.CharField(default='fa-file-o', max_length=25, verbose_name='icon', choices=[('fa-file-o', 'default'), ('fa-file-archive-o', 'archive'), ('fa-file-audio-o', 'audio'), ('fa-file-code-o', 'code'), ('fa-file-excel-o', 'excel'), ('fa-file-image-o', 'image'), ('fa-file-pdf-o', 'pdf'), ('fa-file-powerpoint-o', 'powerpoint'), ('fa-file-text-o', 'text'), ('fa-file-video-o', 'video'), ('fa-file-word-o', 'word'), ('fa-folder-open-o', 'directory')])),
                ('mime_type', models.CharField(max_length=255, verbose_name='mime-type', db_index=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='mime_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='mime-type', null=True, to='snapshots.IconMapping'),
        ),
        migrations.CreateModel(
            name='NasmanTree',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, blank=True, verbose_name='Title', help_text='Site tree title for presentational purposes.')),
                ('alias', models.CharField(max_length=80, unique=True, db_index=True, verbose_name='Alias', help_text='Short name to address site tree from templates.<br /><b>Note:</b> change with care.')),
            ],
            options={
                'verbose_name_plural': 'Site Trees',
                'verbose_name': 'Site Tree',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NasmanTreeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='Title', help_text='Site tree item title. Can contain template variables E.g.: {{ mytitle }}.')),
                ('hint', models.CharField(default='', max_length=200, blank=True, verbose_name='Hint', help_text='Some additional information about this item that is used as a hint.')),
                ('url', models.CharField(max_length=200, db_index=True, verbose_name='URL', help_text='Exact URL or URL pattern (see "Additional settings") for this item.')),
                ('urlaspattern', models.BooleanField(default=False, help_text='Whether the given URL should be treated as a pattern.<br /><b>Note:</b> Refer to Django "URL dispatcher" documentation (e.g. "Naming URL patterns" part).', db_index=True, verbose_name='URL as Pattern')),
                ('hidden', models.BooleanField(default=False, help_text='Whether to show this item in navigation.', db_index=True, verbose_name='Hidden')),
                ('alias', sitetree.models.CharFieldNullable(help_text='Short name to address site tree item from a template.<br /><b>Reserved aliases:</b> "trunk", "this-children", "this-siblings", "this-ancestor-children", "this-parent-siblings".', blank=True, verbose_name='Alias', max_length=80, null=True, db_index=True)),
                ('description', models.TextField(default='', help_text='Additional comments on this item.', blank=True, verbose_name='Description')),
                ('inmenu', models.BooleanField(default=True, help_text='Whether to show this item in a menu.', db_index=True, verbose_name='Show in menu')),
                ('inbreadcrumbs', models.BooleanField(default=True, help_text='Whether to show this item in a breadcrumb path.', db_index=True, verbose_name='Show in breadcrumb path')),
                ('insitetree', models.BooleanField(default=True, help_text='Whether to show this item in a site tree.', db_index=True, verbose_name='Show in site tree')),
                ('access_loggedin', models.BooleanField(default=False, help_text='Check it to grant access to this item to authenticated users only.', db_index=True, verbose_name='Logged in only')),
                ('access_guest', models.BooleanField(default=False, help_text='Check it to grant access to this item to guests only.', db_index=True, verbose_name='Guests only')),
                ('access_restricted', models.BooleanField(default=False, help_text='Check it to restrict user access to this item, using Django permissions system.', db_index=True, verbose_name='Restrict access to permissions')),
                ('access_perm_type', models.IntegerField(default=1, help_text='<b>Any</b> &mdash; user should have any of chosen permissions. <b>All</b> &mdash; user should have all chosen permissions.', verbose_name='Permissions interpretation', choices=[(1, 'Any'), (2, 'All')])),
                ('sort_order', models.IntegerField(default=0, help_text='Item position among other site tree items under the same parent.', db_index=True, verbose_name='Sort order')),
                ('icon', fontawesome.fields.IconField(max_length=60, blank=True, verbose_name='icon')),
                ('access_permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='Permissions granting access')),
                ('parent', models.ForeignKey(help_text='Parent site tree item.', blank=True, related_name='nasmantreeitem_parent', verbose_name='Parent', null=True, to='snapshots.NasmanTreeItem')),
                ('tree', models.ForeignKey(help_text='Site tree this item belongs to.', related_name='nasmantreeitem_tree', verbose_name='Site Tree', to='snapshots.NasmanTree')),
            ],
            options={
                'verbose_name_plural': 'Site Tree Items',
                'verbose_name': 'Site Tree Item',
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='file',
            name='full_path',
            field=nasman.snapshots.models.PathField(verbose_name='full path'),
        ),
        migrations.AlterUniqueTogether(
            name='nasmantreeitem',
            unique_together=set([('tree', 'alias')]),
        ),
        migrations.AlterField(
            model_name='nasmantreeitem',
            name='icon',
            field=fontawesome.fields.IconField(default='circle-o', max_length=60, blank=True, verbose_name='icon'),
        ),
    ]
