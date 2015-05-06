from datetime import datetime
import logging
from celery import shared_task
from pathlib import Path
import chardet

from .models import File
from .utils.zfs import ZFSUtil

logger = logging.getLogger(__name__)


def build_file_list(path):
    """
    Build a list a list of files (and directories) by iterating recursively
    over the given path
    :param path: The path to iterate over
    :type path: pathlib.Path
    :return: A tuple of directories and files
    :rtype: tuple(list, list)
    """
    dirs = []
    files = []
    for x in path.iterdir():
        try:
            if x.is_symlink():
                continue
            elif x.is_dir():
                dirs.append(x)
                new_dirs, new_files = build_file_list(x)
                dirs.extend(new_dirs)
                files.extend(new_files)
            elif x.is_file():
                files.append(x)
        except PermissionError:
            continue
    return dirs, files

def collect_files(path):
    """
    Recursively add all files and directories of the given path to the
    database
    :param path: The path to iterate over recursively
    :type path: pathlib.Path
    """
    logger.info('Building file list...')
    start_time = datetime.now()
    dirs, files = build_file_list(path)
    seconds = (datetime.now() - start_time).total_seconds()
    logger.info(
        'Found %d files and directories in %.3fs',
        (len(dirs) + len(files)),
        seconds
    )
    return dirs, files


@shared_task
def index_snapshot(snap_name):
    snap = ZFSUtil.get_snapshot(snap_name)
    fs = snap.filesystem
    fs_root = Path(fs._mountpoint)
    if not snap.is_mounted:
        snap.mount()
    dirs, files = collect_files(snap.mountpoint)
    logger.info('Saving files to database')
    for x in dirs + files:
        orig_path = fs_root.joinpath(x.relative_to(fs.mountpoint))
        encoding = chardet.detect(bytes(x))['encoding']
        obj = File(
            snapshot_path=str(x).encode(
                'utf-8',
                'surrogateescape').decode(self.path_encoding),
            original_path=str(orig_path),
            snapshot_name=snap_name
        )
        obj.save()

