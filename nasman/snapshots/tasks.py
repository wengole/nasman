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


@shared_task(bind=True, track_started=True)
def walk_and_reindex(self, path):
    """
    Task to walk a given path and index all files and directories within it
    """
    self.total_files = 0
    self.groups = []
    self.update_count = 0
    self.update_rate = 10

    def jobs(self):
        """
        The individual jobs in all groups currently queued
        """
        return [job for group in self.groups for job in group.children]

    def done_files(self):
        """
        The number of files that have been indexed so far
        """
        done = sum([int(x.ready()) for x in jobs(self)])
        return done

    def work_to_do(self):
        """
        Are there any outstanding jobs to complete?
        """
        to_do = any([not job.ready() for job in self.groups])
        return to_do

    def update_progress(self):
        """
        Set the task state to PROGRESS and add metadata about the progress of
        the task
        """
        if self.update_count < self.update_rate:
            self.update_count += 1
            return
        self.update_count = 0
        done = Decimal(done_files(self))
        total = Decimal(self.total_files)
        self.update_state(
            state=states.STARTED,
            meta={
                'percentage': done / total * 100 if total > 0 else 100,
                'done': done_files(self),
                'total': self.total_files
            }
        )

    # Don't reindex this path if there's a reindex in progress
    cache_key = 'reindex_status%s' % hashlib.sha1(path.encode('utf-8')).hexdigest()[-6:]
    cached = cache.get(cache_key)
    if cached is not None and cached.state == 'RUNNING':
        message = 'Already reindexing %s' % path
        logger.warn(message)
        raise AlreadyRunning(message)

    for dirname, subdirs, files in os.walk(path):
        logger.info('Adding subdirs for %s', dirname)
        self.total_files += len(subdirs)
        subdirs_job = group([create_file_object.s(
            full_path=os.path.join(dirname, s),
            directory=True
        ) for s in subdirs])
        self.groups.append(subdirs_job.apply_async())
        update_progress(self)

        logger.info('Adding files for %s', dirname)
        self.total_files += len(files)
        files_job = group([create_file_object.s(
            full_path=os.path.join(dirname, f)
        ) for f in files])
        self.groups.append(files_job.apply_async())
        update_progress(self)

    update_progress(self)
    logger.info('All files and directories queued')
    if work_to_do(self):
        logger.debug('Still waiting on %d jobs',
                     self.total_files - done_files(self))

    while work_to_do(self):
        update_progress(self)
        logger.debug('Still waiting on %d jobs',
                     self.total_files - done_files(self))
    done = Decimal(done_files(self))
    total = Decimal(self.total_files)
    return {
        'percentage': done / total * 100 if total > 0 else 100,
        'done': done_files(self),
        'total': self.total_files
    }
