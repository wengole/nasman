# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fontawesome.fields
import sitetree.models


class Migration(migrations.Migration):

    dependencies = [
        ('sitetree', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('snapshot_path', models.TextField(help_text='The path to the file when the relevant snapshot is mounted', verbose_name='snapshot path')),
                ('original_path', models.TextField(help_text='The original path on the filesystem when the snapshot was taken', verbose_name='original path')),
                ('snapshot_name', models.TextField(help_text='Name of the snapshot', verbose_name='snapshot name')),
            ],
        ),
        migrations.CreateModel(
            name='IconMapping',
            fields=[
                ('icon', fontawesome.fields.IconField(blank=True, default='fa-file-o', max_length=60, verbose_name='icon')),
                ('mime_type', models.CharField(primary_key=True, max_length=255, serialize=False, verbose_name='mime-type', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='NasmanTreeItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(help_text='Site tree item title. Can contain template variables E.g.: {{ mytitle }}.', verbose_name='Title', max_length=100)),
                ('hint', models.CharField(help_text='Some additional information about this item that is used as a hint.', blank=True, default='', max_length=200, verbose_name='Hint')),
                ('url', models.CharField(help_text='Exact URL or URL pattern (see "Additional settings") for this item.', max_length=200, verbose_name='URL', db_index=True)),
                ('urlaspattern', models.BooleanField(help_text='Whether the given URL should be treated as a pattern.<br /><b>Note:</b> Refer to Django "URL dispatcher" documentation (e.g. "Naming URL patterns" part).', default=False, db_index=True, verbose_name='URL as Pattern')),
                ('hidden', models.BooleanField(help_text='Whether to show this item in navigation.', default=False, db_index=True, verbose_name='Hidden')),
                ('alias', sitetree.models.CharFieldNullable(help_text='Short name to address site tree item from a template.<br /><b>Reserved aliases:</b> "trunk", "this-children", "this-siblings", "this-ancestor-children", "this-parent-siblings".', null=True, blank=True, db_index=True, verbose_name='Alias', max_length=80)),
                ('description', models.TextField(help_text='Additional comments on this item.', blank=True, default='', verbose_name='Description')),
                ('inmenu', models.BooleanField(help_text='Whether to show this item in a menu.', default=True, db_index=True, verbose_name='Show in menu')),
                ('inbreadcrumbs', models.BooleanField(help_text='Whether to show this item in a breadcrumb path.', default=True, db_index=True, verbose_name='Show in breadcrumb path')),
                ('insitetree', models.BooleanField(help_text='Whether to show this item in a site tree.', default=True, db_index=True, verbose_name='Show in site tree')),
                ('access_loggedin', models.BooleanField(help_text='Check it to grant access to this item to authenticated users only.', default=False, db_index=True, verbose_name='Logged in only')),
                ('access_guest', models.BooleanField(help_text='Check it to grant access to this item to guests only.', default=False, db_index=True, verbose_name='Guests only')),
                ('access_restricted', models.BooleanField(help_text='Check it to restrict user access to this item, using Django permissions system.', default=False, db_index=True, verbose_name='Restrict access to permissions')),
                ('access_perm_type', models.IntegerField(help_text='<b>Any</b> &mdash; user should have any of chosen permissions. <b>All</b> &mdash; user should have all chosen permissions.', default=1, choices=[(1, 'Any'), (2, 'All')], verbose_name='Permissions interpretation')),
                ('sort_order', models.IntegerField(help_text='Item position among other site tree items under the same parent.', default=0, db_index=True, verbose_name='Sort order')),
                ('icon', fontawesome.fields.IconField(blank=True, default='circle-o', max_length=60, verbose_name='icon')),
                ('access_permissions', models.ManyToManyField(blank=True, verbose_name='Permissions granting access', to='auth.Permission')),
                ('parent', models.ForeignKey(help_text='Parent site tree item.', null=True, blank=True, to='snapshots.NasmanTreeItem', related_name='nasmantreeitem_parent', verbose_name='Parent')),
                ('tree', models.ForeignKey(help_text='Site tree this item belongs to.', to='sitetree.Tree', related_name='nasmantreeitem_tree', verbose_name='Site Tree')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Site Tree Item',
                'verbose_name_plural': 'Site Tree Items',
            },
        ),
        migrations.AlterUniqueTogether(
            name='nasmantreeitem',
            unique_together=set([('tree', 'alias')]),
        ),
    ]
