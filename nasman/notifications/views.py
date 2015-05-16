import datetime
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Notification
from .serializers import NotificationSerializer


class NotificationPagination(LimitOffsetPagination):
    default_limit = 10


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination
    base_queryset = Notification.objects.all().order_by('-created')

    def get_queryset(self):
        qs = self.base_queryset
        since = self.request.query_params.get('since', None)
        if since is None:
            return qs
        return qs.filter(created__gt=since)

    def list(self, request, *args, **kwargs):
        response = super(NotificationViewSet, self).list(
            request,
            *args,
            **kwargs)
        response.data['latest'] = self.base_queryset.latest(
            'created').created + datetime.timedelta(seconds=1)
        return response
