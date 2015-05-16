from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Notification
from .serializers import NotificationSerializer


class NotificationPagination(LimitOffsetPagination):
    default_limit = 10


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination
    def list(self, request, *args, **kwargs):
        response = super(NotificationViewSet, self).list(
            request,
            *args,
            **kwargs)
        response.data['latest'] = self.base_queryset.latest(
            'created').created + datetime.timedelta(seconds=1)
        return response
