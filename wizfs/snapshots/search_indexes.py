from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from snapshots.models import Snapshot, File


class SnapshotIndex(CelerySearchIndex, indexes.Indexable):
    """
    Indexer for ``Snapshot`` objects
    """
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr=u'name')
    timestamp = indexes.DateTimeField(model_attr=u'timestamp', null=True)

    def get_model(self):
        return Snapshot


class FileIndex(CelerySearchIndex, indexes.Indexable):
    """
    Indexer for ``File`` objects
    """
    text = indexes.CharField(document=True, use_template=True)
    directory = indexes.CharField(model_attr=u'dirname', faceted=True)
    name = indexes.CharField(model_attr=u'name')
    snapshot = indexes.CharField(
        model_attr=u'snapshot__name',
        null=True,
        faceted=True
    )

    def get_model(self):
        return File
