from datetime import datetime
from decimal import Decimal
import logging

import hashlib
import os
import magic
from celery import group, shared_task, states
from django.core.cache import cache
from django.utils.timezone import get_default_timezone_name
import pytz

from .models import File, IconMapping


logger = logging.getLogger(__name__)


class AlreadyRunning(Exception):
    pass


@shared_task(name='nasman.snapshots.tasks.create_file_object')
def create_file_object(full_path, snapshot=None, directory=False):
    logger.info('Adding %s: %s',
                ('directory' if directory else 'file'), full_path)
    statinfo = os.stat(full_path)
    mtime = datetime.fromtimestamp(statinfo.st_mtime)
    mtime = pytz.timezone(get_default_timezone_name()).localize(mtime)
    try:
        magic_info = magic.from_file(full_path)
    except magic.MagicException:
        magic_info = ''
    try:
        mime_type = magic.from_file(full_path, mime=True)
    except magic.MagicException:
        icon = None
    else:
        icon, _ = IconMapping.objects.get_or_create(
            mime_type=mime_type
        )
    obj, created = File.objects.get_or_create(
        full_path=full_path,
        snapshot=snapshot,
        directory=directory,
        defaults={
            'name': os.path.basename(full_path),
            'dirname': os.path.dirname(full_path),
            'mime_type': icon,
            'magic': magic_info,
            'modified': mtime,
            'size': statinfo.st_size,
        }
    )
    if not created:
        obj.mime_type = icon
        obj.magic = magic_info
        obj.modified = mtime
        obj.size = statinfo.st_size
        obj.save()


@shared_task
def walk_and_index(path):
    """
    Recursive task for walking a filesystem tree and adding files to the
    database
    :param path: The path to start walking from
    :type path: pathlib.Path
    """
    dirs = []
    files = []
    for x in path.iterdir():
        if not x.exists():
            logger.warn('%s does not exist, skipping indexing', x)
            continue
        if x.is_dir():
            dirs.append(x)
            walk_and_index(x)
        if x.is_file():
            files.append(x)
    dir_tasks = [[
        x,
        None,
        True
    ] for x in dirs]
    create_file_object.chunks(dir_tasks, 10)
