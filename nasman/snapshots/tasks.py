from datetime import datetime
import logging

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
    # print('{0} contained {1} dirs and {2} files'.format(
    #     str(path), len(dirs), len(files)
    # ))
    return dirs, files

def index_path(path):
    """
    Recursively add all files and directories of the given path to the
    database
    :param path: The path to iterate over recursively
    :type path: pathlib.Path
    """
    logger.info('Building file list...')
    print('Building file list...')
    start_time = datetime.now()
    dirs, files = build_file_list(path)
    seconds = (datetime.now() - start_time).total_seconds()
    logger.info(
        'Found {0} dirs and {1} files in {2}s', len(dirs), len(files), seconds
    )
    print(
        'Found {0} dirs and {1} files in {2}s'.format(len(dirs), len(files), seconds)
    )
