# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sitetree.models
import nasman.snapshots.models
import django.db.models.deletion
import djorm_pgfulltext.fields
import fontawesome.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('sitetree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('full_path', nasman.snapshots.models.PathField(verbose_name='full path')),
                ('dirname', models.TextField(db_index=True, verbose_name='dirname')),
                ('name', models.TextField(db_index=True, verbose_name='name')),
                ('snapshot_name', models.TextField(db_index=True, verbose_name='snapshot')),
                ('directory', models.BooleanField(default=False)),
                ('magic', models.CharField(max_length=255, blank=True, verbose_name='magic')),
                ('modified', models.DateTimeField(verbose_name='modified')),
                ('size', models.IntegerField(blank=True, verbose_name='size', null=True)),
                ('search_index', djorm_pgfulltext.fields.VectorField(null=True, editable=False, db_index=True, default='', serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='IconMapping',
            fields=[
                ('icon', models.CharField(max_length=25, default='fa-file-o', choices=[('fa-file-o', 'default'), ('fa-file-archive-o', 'archive'), ('fa-file-audio-o', 'audio'), ('fa-file-code-o', 'code'), ('fa-file-excel-o', 'excel'), ('fa-file-image-o', 'image'), ('fa-file-pdf-o', 'pdf'), ('fa-file-powerpoint-o', 'powerpoint'), ('fa-file-text-o', 'text'), ('fa-file-video-o', 'video'), ('fa-file-word-o', 'word'), ('fa-folder-open-o', 'directory')], verbose_name='icon')),
                ('mime_type', models.CharField(max_length=255, db_index=True, verbose_name='mime-type', serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='NasmanTreeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title', help_text='Site tree item title. Can contain template variables E.g.: {{ mytitle }}.')),
                ('hint', models.CharField(help_text='Some additional information about this item that is used as a hint.', max_length=200, blank=True, default='', verbose_name='Hint')),
                ('url', models.CharField(max_length=200, db_index=True, verbose_name='URL', help_text='Exact URL or URL pattern (see "Additional settings") for this item.')),
                ('urlaspattern', models.BooleanField(help_text='Whether the given URL should be treated as a pattern.<br /><b>Note:</b> Refer to Django "URL dispatcher" documentation (e.g. "Naming URL patterns" part).', db_index=True, default=False, verbose_name='URL as Pattern')),
                ('hidden', models.BooleanField(help_text='Whether to show this item in navigation.', db_index=True, default=False, verbose_name='Hidden')),
                ('alias', sitetree.models.CharFieldNullable(db_index=True, blank=True, max_length=80, verbose_name='Alias', null=True, help_text='Short name to address site tree item from a template.<br /><b>Reserved aliases:</b> "trunk", "this-children", "this-siblings", "this-ancestor-children", "this-parent-siblings".')),
                ('description', models.TextField(help_text='Additional comments on this item.', blank=True, default='', verbose_name='Description')),
                ('inmenu', models.BooleanField(help_text='Whether to show this item in a menu.', db_index=True, default=True, verbose_name='Show in menu')),
                ('inbreadcrumbs', models.BooleanField(help_text='Whether to show this item in a breadcrumb path.', db_index=True, default=True, verbose_name='Show in breadcrumb path')),
                ('insitetree', models.BooleanField(help_text='Whether to show this item in a site tree.', db_index=True, default=True, verbose_name='Show in site tree')),
                ('access_loggedin', models.BooleanField(help_text='Check it to grant access to this item to authenticated users only.', db_index=True, default=False, verbose_name='Logged in only')),
                ('access_guest', models.BooleanField(help_text='Check it to grant access to this item to guests only.', db_index=True, default=False, verbose_name='Guests only')),
                ('access_restricted', models.BooleanField(help_text='Check it to restrict user access to this item, using Django permissions system.', db_index=True, default=False, verbose_name='Restrict access to permissions')),
                ('access_perm_type', models.IntegerField(help_text='<b>Any</b> &mdash; user should have any of chosen permissions. <b>All</b> &mdash; user should have all chosen permissions.', default=1, choices=[(1, 'Any'), (2, 'All')], verbose_name='Permissions interpretation')),
                ('sort_order', models.IntegerField(help_text='Item position among other site tree items under the same parent.', db_index=True, default=0, verbose_name='Sort order')),
                ('icon', fontawesome.fields.IconField(max_length=60, blank=True, default='circle-o', verbose_name='icon')),
                ('access_permissions', models.ManyToManyField(to='auth.Permission', blank=True, verbose_name='Permissions granting access')),
                ('parent', models.ForeignKey(blank=True, related_name='nasmantreeitem_parent', help_text='Parent site tree item.', to='snapshots.NasmanTreeItem', verbose_name='Parent', null=True)),
                ('tree', models.ForeignKey(related_name='nasmantreeitem_tree', help_text='Site tree this item belongs to.', to='sitetree.Tree', verbose_name='Site Tree')),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='snapshots.IconMapping', verbose_name='mime-type', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='nasmantreeitem',
            unique_together=set([('tree', 'alias')]),
        ),
    ]
