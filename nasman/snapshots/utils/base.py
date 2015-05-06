import pathlib
import abc
import chardet

from django.utils.timezone import get_default_timezone_name, now


def decode_from_filesystem(path):
    """
    Decode a given Path object to unicode by detecting its encoding
    :param path: The Path object to decode
    :type path: pathlib.Path
    :return: Tuple of the str representation of the path, and it's original
        codec name
    :rtype: tuple
    """
    value = str(path)
    b = bytes(path)
    codec = chardet.detect(b)['encoding']
    return value.encode('utf-8', 'surrogateescape').decode(codec), codec

def encode_to_filesystem(value, codec):
    """
    Encode the given value using the given codec back Path object
    :param value: Unicode represented path
    :type value: str
    :param codec: Originally detected codec
    :type codec: str
    :return: Path object
    :rtype: pathlib.Path
    """
    return pathlib.Path(value.encode(codec).decode('utf-8', 'surrogateescape'))


class BaseFilesystem(metaclass=abc.ABCMeta):

    def __init__(self, name, mountpoint=''):
        self._name = name
        self._mountpoint = mountpoint

    @property
    @abc.abstractmethod
    def name(self):
        """
        :return: The name of the filesystem
        :rtype: basestring
        """

    @property
    @abc.abstractmethod
    def mountpoint(self):
        """
        :return: The mountpoint of the filesystem
        :rtype: basestring
        """


class BaseSnapshot(metaclass=abc.ABCMeta):

    def __init__(self, name, timestamp=None, filesystem=None):
        self._name = name
        self._filesystem = filesystem
        if timestamp is not None:
            self._timestamp = timestamp
        else:
            self._timestamp = now()

    @property
    @abc.abstractmethod
    def name(self):
        """
        :return: The name of the snapshot
        :rtype: basestring
        """

    @property
    @abc.abstractmethod
    def timestamp(self):
        """
        :return: The creation time of this snapshot
        :rtype: `datetime.datetime`
        """

    @property
    @abc.abstractmethod
    def filesystem(self):
        """
        :return: The parent filesystem of this snapshot
        :rtype: `BaseFilesystem`
        """


class BaseUtil(metaclass=abc.ABCMeta):
    timezone_name = get_default_timezone_name()

    @classmethod
    @abc.abstractmethod
    def get_filesystems(cls):
        """
        Gets a list of filesystems
        :return: A list of `BaseFilesystem` objects
        :rtype: list
        """

    @classmethod
    @abc.abstractmethod
    def get_snapshots(cls):
        """
        Gets a list of snapshots
        :return: A list of `BaseSnapshot`
        :rtype: list
        """
