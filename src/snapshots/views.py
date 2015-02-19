from django.views.generic import ListView
from snapshots.models import Snapshot


class SnapshotListView(ListView):
    model = Snapshot