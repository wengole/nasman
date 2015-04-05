from datetime import datetime

from haystack.utils.loading import UnifiedIndex
from django.test import override_settings, TestCase
import haystack
from haystack.query import SearchQuerySet
from snapshots.models import Snapshot, Filesystem
from snapshots.search_indexes import SnapshotIndex


TEST_INDEX = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': 'test_index',
    },
}


@override_settings(HAYSTACK_CONNECTIONS=TEST_INDEX)
class SearchQuerySetTestCase(TestCase):

    def setUp(self):
        super(SearchQuerySetTestCase, self).setUp()

        # Stow.
        self.old_unified_index = haystack.connections['default']._index
        self.ui = UnifiedIndex()
        self.ui.build()
        haystack.connections['default']._index = self.ui

        # Update the "index".
        backend = haystack.connections['default'].get_backend()
        backend.clear()
        backend.update(SnapshotIndex, Snapshot.objects.all())

        self.msqs = SearchQuerySet()

        # Stow.
        haystack.reset_search_queries()

    def tearDown(self):
        # Restore.
        haystack.connections['default']._index = self.old_unified_index
        super(SearchQuerySetTestCase, self).tearDown()

    def test_snapshot_is_indexed(self):
        sqs = SearchQuerySet().all()
        self.assertEqual(sqs.count(), 0)
        fs = Filesystem.objects.create(
            name='foo',
            parent=None,
            mountpoint='/foo'
        )
        Snapshot.objects.create(
            name='test_snap_1',
            timestamp=datetime.now(),
            filesystem=fs
        )
        sqs = SearchQuerySet().all()
        self.assertEqual(sqs.count(), 1)
