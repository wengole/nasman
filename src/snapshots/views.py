from django.views.generic import ListView, TemplateView
from snapshots.models import Snapshot


class SnapshotListView(ListView):
    model = Snapshot
