import abc

from django.utils.timezone import get_default_timezone_name, now


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
