from vanilla import ListView
from .models import Notification
from nasman.snapshots.views.base import BaseView


class Notifications(BaseView, ListView):
    model = Notification
    template_name = 'home.html'
    headline = 'Notifications Demo'

    def get_queryset(self):
        return self.model.objects.order_by('-pk')[:5]
