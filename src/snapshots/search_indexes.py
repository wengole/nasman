from haystack import indexes

from .models import Snapshot


class SnapshotIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Indexer for ``Snapshot`` objects
    """
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    timestamp = indexes.DateTimeField(model_attr='timestamp', null=True)

    def get_model(self):
        return Snapshot