from __future__ import absolute_import
from datetime import datetime
from django.utils.timezone import get_default_timezone_name
import os

from celery import task
import magic
import pytz

from .models import File


@task
def create_file_object(full_path, snapshot=None, directory=False):
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
        mime_type = ''
    File.objects.get_or_create(
        full_path=full_path,
        snapshot=snapshot,
        directory=directory,
        mime_type=mime_type,
        magic=magic_info,
        modified=mtime,
        size=statinfo.st_size,
    )
