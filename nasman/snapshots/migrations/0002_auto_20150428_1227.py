# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fontawesome.fields
import sitetree.models
import nasman.snapshots.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('snapshots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NasmanTree',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(help_text='Site tree title for presentational purposes.', max_length=100, verbose_name='Title', blank=True)),
                ('alias', models.CharField(db_index=True, unique=True, max_length=80, verbose_name='Alias', help_text='Short name to address site tree from templates.<br /><b>Note:</b> change with care.')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Site Trees',
                'verbose_name': 'Site Tree',
            },
        ),
        migrations.CreateModel(
            name='NasmanTreeItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(help_text='Site tree item title. Can contain template variables E.g.: {{ mytitle }}.', max_length=100, verbose_name='Title')),
                ('hint', models.CharField(default='', blank=True, max_length=200, verbose_name='Hint', help_text='Some additional information about this item that is used as a hint.')),
                ('url', models.CharField(db_index=True, help_text='Exact URL or URL pattern (see "Additional settings") for this item.', max_length=200, verbose_name='URL')),
                ('urlaspattern', models.BooleanField(db_index=True, default=False, verbose_name='URL as Pattern', help_text='Whether the given URL should be treated as a pattern.<br /><b>Note:</b> Refer to Django "URL dispatcher" documentation (e.g. "Naming URL patterns" part).')),
                ('hidden', models.BooleanField(db_index=True, default=False, verbose_name='Hidden', help_text='Whether to show this item in navigation.')),
                ('alias', sitetree.models.CharFieldNullable(db_index=True, help_text='Short name to address site tree item from a template.<br /><b>Reserved aliases:</b> "trunk", "this-children", "this-siblings", "this-ancestor-children", "this-parent-siblings".', max_length=80, verbose_name='Alias', blank=True, null=True)),
                ('description', models.TextField(default='', blank=True, verbose_name='Description', help_text='Additional comments on this item.')),
                ('inmenu', models.BooleanField(db_index=True, default=True, verbose_name='Show in menu', help_text='Whether to show this item in a menu.')),
                ('inbreadcrumbs', models.BooleanField(db_index=True, default=True, verbose_name='Show in breadcrumb path', help_text='Whether to show this item in a breadcrumb path.')),
                ('insitetree', models.BooleanField(db_index=True, default=True, verbose_name='Show in site tree', help_text='Whether to show this item in a site tree.')),
                ('access_loggedin', models.BooleanField(db_index=True, default=False, verbose_name='Logged in only', help_text='Check it to grant access to this item to authenticated users only.')),
                ('access_guest', models.BooleanField(db_index=True, default=False, verbose_name='Guests only', help_text='Check it to grant access to this item to guests only.')),
                ('access_restricted', models.BooleanField(db_index=True, default=False, verbose_name='Restrict access to permissions', help_text='Check it to restrict user access to this item, using Django permissions system.')),
                ('access_perm_type', models.IntegerField(choices=[(1, 'Any'), (2, 'All')], default=1, verbose_name='Permissions interpretation', help_text='<b>Any</b> &mdash; user should have any of chosen permissions. <b>All</b> &mdash; user should have all chosen permissions.')),
                ('sort_order', models.IntegerField(db_index=True, default=0, verbose_name='Sort order', help_text='Item position among other site tree items under the same parent.')),
                ('icon', fontawesome.fields.IconField(max_length=60, verbose_name='icon', blank=True)),
                ('access_permissions', models.ManyToManyField(to='auth.Permission', verbose_name='Permissions granting access', blank=True)),
                ('parent', models.ForeignKey(help_text='Parent site tree item.', related_name='nasmantreeitem_parent', verbose_name='Parent', blank=True, to='snapshots.NasmanTreeItem', null=True)),
                ('tree', models.ForeignKey(help_text='Site tree this item belongs to.', related_name='nasmantreeitem_tree', verbose_name='Site Tree', to='snapshots.NasmanTree')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Site Tree Items',
                'verbose_name': 'Site Tree Item',
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
    ]
