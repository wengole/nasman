# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sitetree.models
import fontawesome.fields
import djorm_pgfulltext.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('sitetree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('snapshot_path', models.TextField(verbose_name='snapshot path', help_text='The path to the file when the relevant snapshot is mounted')),
                ('original_path', models.TextField(verbose_name='original path', help_text='The original path on the filesystem when the snapshot was taken')),
                ('snapshot_name', models.TextField(verbose_name='snapshot name', help_text='Name of the snapshot')),
                ('path_encoding', models.TextField(blank=True, verbose_name='path encoding', help_text='The filesystem encoding for this file')),
                ('search_index', djorm_pgfulltext.fields.VectorField(serialize=False, null=True, db_index=True, editable=False, default='')),
            ],
        ),
        migrations.CreateModel(
            name='IconMapping',
            fields=[
                ('icon', fontawesome.fields.IconField(max_length=60, blank=True, verbose_name='icon', default='fa-file-o')),
                ('mime_type', models.CharField(max_length=255, serialize=False, primary_key=True, db_index=True, verbose_name='mime-type')),
            ],
        ),
        migrations.CreateModel(
            name='NasmanTreeItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title', help_text='Site tree item title. Can contain template variables E.g.: {{ mytitle }}.')),
                ('hint', models.CharField(max_length=200, default='', blank=True, verbose_name='Hint', help_text='Some additional information about this item that is used as a hint.')),
                ('url', models.CharField(max_length=200, db_index=True, verbose_name='URL', help_text='Exact URL or URL pattern (see "Additional settings") for this item.')),
                ('urlaspattern', models.BooleanField(default=False, db_index=True, verbose_name='URL as Pattern', help_text='Whether the given URL should be treated as a pattern.<br /><b>Note:</b> Refer to Django "URL dispatcher" documentation (e.g. "Naming URL patterns" part).')),
                ('hidden', models.BooleanField(default=False, db_index=True, verbose_name='Hidden', help_text='Whether to show this item in navigation.')),
                ('alias', sitetree.models.CharFieldNullable(null=True, db_index=True, blank=True, verbose_name='Alias', help_text='Short name to address site tree item from a template.<br /><b>Reserved aliases:</b> "trunk", "this-children", "this-siblings", "this-ancestor-children", "this-parent-siblings".', max_length=80)),
                ('description', models.TextField(default='', blank=True, verbose_name='Description', help_text='Additional comments on this item.')),
                ('inmenu', models.BooleanField(default=True, db_index=True, verbose_name='Show in menu', help_text='Whether to show this item in a menu.')),
                ('inbreadcrumbs', models.BooleanField(default=True, db_index=True, verbose_name='Show in breadcrumb path', help_text='Whether to show this item in a breadcrumb path.')),
                ('insitetree', models.BooleanField(default=True, db_index=True, verbose_name='Show in site tree', help_text='Whether to show this item in a site tree.')),
                ('access_loggedin', models.BooleanField(default=False, db_index=True, verbose_name='Logged in only', help_text='Check it to grant access to this item to authenticated users only.')),
                ('access_guest', models.BooleanField(default=False, db_index=True, verbose_name='Guests only', help_text='Check it to grant access to this item to guests only.')),
                ('access_restricted', models.BooleanField(default=False, db_index=True, verbose_name='Restrict access to permissions', help_text='Check it to restrict user access to this item, using Django permissions system.')),
                ('access_perm_type', models.IntegerField(default=1, help_text='<b>Any</b> &mdash; user should have any of chosen permissions. <b>All</b> &mdash; user should have all chosen permissions.', verbose_name='Permissions interpretation', choices=[(1, 'Any'), (2, 'All')])),
                ('sort_order', models.IntegerField(default=0, db_index=True, verbose_name='Sort order', help_text='Item position among other site tree items under the same parent.')),
                ('icon', fontawesome.fields.IconField(max_length=60, blank=True, verbose_name='icon', default='circle-o')),
                ('access_permissions', models.ManyToManyField(to='auth.Permission', blank=True, verbose_name='Permissions granting access')),
                ('parent', models.ForeignKey(null=True, blank=True, verbose_name='Parent', help_text='Parent site tree item.', to='snapshots.NasmanTreeItem', related_name='nasmantreeitem_parent')),
                ('tree', models.ForeignKey(verbose_name='Site Tree', help_text='Site tree this item belongs to.', to='sitetree.Tree', related_name='nasmantreeitem_tree')),
            ],
            options={
                'verbose_name': 'Site Tree Item',
                'verbose_name_plural': 'Site Tree Items',
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='nasmantreeitem',
            unique_together=set([('tree', 'alias')]),
        ),
    ]
