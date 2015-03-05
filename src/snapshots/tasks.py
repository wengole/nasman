from __future__ import absolute_import
from datetime import datetime
import logging
from time import sleep
import os

from celery import task, group, Task
from django.utils.timezone import get_default_timezone_name
import magic
import pytz

from .models import File, Filesystem


logger = logging.getLogger(__name__)


@task(bind=True)
def create_file_object(self, full_path, snapshot=None, directory=False):
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


@task
def reindex_filesystem(fs_name):
    """
    Task to walk a given filesystem (which may be a snapshot) and index all
    files and directories within it
    """
    total_files = 0
    groups = []

    @property
    def jobs(self):
        """
        The individual jobs in all groups currently queued
        """
        return [job for group in self.groups for job in group.children]

    @property
    def done_files(self):
        """
        The number of files that have been indexed so far
        """
        done = sum([int(x.ready()) for x in self.jobs])
        return done

    @property
    def work_to_do(self):
        to_do = any([not job.ready() for job in self.groups])
        return to_do

    try:
        fs = Filesystem.objects.get(
            name=fs_name
        )
    except Filesystem.DoesNotExist:
        logger.error('Filesystem "%s" does not exist', fs_name)
        return
    for dirname, subdirs, files in fs.walk_fs():
        logger.info('Adding subdirs for %s', dirname)
        total_files += len(subdirs)
        subdirs_job = group([create_file_object.s(
            full_path=u'%s/%s' % (dirname, s),
            directory=True
        ) for s in subdirs])
        groups.append(subdirs_job.apply_async())

        logger.info('Adding files for %s', dirname)
        total_files += len(files)
        files_job = group([create_file_object.s(
            full_path=u'%s/%s' % (dirname, f)
        ) for f in files])
        groups.append(files_job.apply_async())
        update_progress(done_files, total_files, 10)
    logger.info('All files and directories queued')
    if any([not job.ready() for job in groups]):
        logger.info('Still waiting on %d jobs',
                    total_files - done_files)
    while self.work_to_do:
        sleep(5)
        logger.info('Still waiting on %d jobs',
                    self.total_files - self.done_files)


class ReindexFilesystem(Task):
    """
    Task to walk a given filesystem (which may be a snapshot) and index all
    files and directories within it
    """
    significant_kwargs = [
        ('fs_name', str)
    ]
    cache_duration = 0
    # Shouldn't take longer than about 20 minutes
    herd_avoidance_timeout = 1200
    total_files = 0
    groups = []

    @property
    def jobs(self):
        """
        The individual jobs in all groups currently queued
        """
        return [job for group in self.groups for job in group.children]

    @property
    def done_files(self):
        """
        The number of files that have been indexed so far
        """
        done = sum([int(x.ready()) for x in self.jobs])
        return done

    @property
    def work_to_do(self):
        to_do = any([not job.ready() for job in self.groups])
        return to_do

    def run(self, fs_name):
        try:
            fs = Filesystem.objects.get(
                name=fs_name
            )
        except Filesystem.DoesNotExist:
            logger.error('Filesystem "%s" does not exist', fs_name)
            return
        for dirname, subdirs, files in fs.walk_fs():
            logger.info('Adding subdirs for %s', dirname)
            self.total_files += len(subdirs)
            subdirs_job = group([create_file_object.s(
                full_path=u'%s/%s' % (dirname, s),
                directory=True
            ) for s in subdirs])
            self.groups.append(subdirs_job.apply_async())

            logger.info('Adding files for %s', dirname)
            self.total_files += len(files)
            files_job = group([create_file_object.s(
                full_path=u'%s/%s' % (dirname, f)
            ) for f in files])
            self.groups.append(files_job.apply_async())
            self.update_progress(self.done_files, self.total_files, 10)
        logger.info('All files and directories queued')
        if self.work_to_do:
            logger.info('Still waiting on %d jobs',
                        self.total_files - self.done_files)
        while self.work_to_do:
            sleep(5)
            logger.info('Still waiting on %d jobs',
                        self.total_files - self.done_files)
