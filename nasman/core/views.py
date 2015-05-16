import datetime
import logging

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Notification
from nasman.snapshots.models import ZFSFilesystem, ZFSSnapshot
from .serializers import (NotificationSerializer,
                          ZFSFilesystemSerializer,
                          ZFSSnapshotSerializer)

logger = logging.getLogger(__name__)


class NasManPagination(LimitOffsetPagination):
    default_limit = 10


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Viewset for the Notification model
    """
    serializer_class = NotificationSerializer
    pagination_class = NasManPagination
    base_queryset = Notification.objects.all().order_by('-created')

    def get_queryset(self):
        """
        If `since` query parameter exists, only return notifications created
        since the timestamp provided
        :return: The potentially filtered queryset
        :rtype: `QuerySet`
        """
        qs = self.base_queryset
        since = self.request.query_params.get('since', None)
        if since is None:
            return qs
        return qs.filter(created__gt=since)

    def list(self, request, *args, **kwargs):
        """
        Get the list of Notifications and add the `latest` property
        """
        response = super(NotificationViewSet, self).list(
            request,
            *args,
            **kwargs)
        try:
            latest_notification = self.base_queryset.latest('created')
        except Notification.DoesNotExist:
            response.data['latest'] = datetime.datetime(1970, 1, 1)
        else:
            response.data['latest'] = (
                latest_notification.created + datetime.timedelta(seconds=1))
        return response


class ZFSBaseViewSet(viewsets.ModelViewSet):
    pagination_class = NasManPagination
    base_queryset = None

    def refresh_objects(self):
        raise NotImplementedError

    def get_queryset(self):
        qs = self.base_queryset
        refresh = self.request.query_params.get('refresh', False)
        logger.info('Refresh %s', refresh)
        if refresh:
            self.refresh_objects()
        return qs


class ZFSFilesystemViewSet(ZFSBaseViewSet):
    """
    Viewset for ZFSFilesystem
    """
    serializer_class = ZFSFilesystemSerializer
    base_queryset = ZFSFilesystem.objects.all()

    def refresh_objects(self):
        ZFSFilesystem.objects.refresh_from_os()

class ZFSSnapshotViewSet(ZFSBaseViewSet):
    """
    Viewset for ZFSSnapshot
    """
    serializer_class = ZFSSnapshotSerializer
    base_queryset = ZFSSnapshot.objects.all()

    def refresh_objects(self):
        ZFSSnapshot.objects.refresh_from_os()
