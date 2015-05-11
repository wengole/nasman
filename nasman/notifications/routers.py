import logging

from swampdragon import route_handler
from swampdragon.route_handler import ModelPubRouter

from .models import Notification
from .serializers import NotificationSerializer

logger = logging.getLogger(__name__)


class NotificationRouter(ModelPubRouter):
    route_name = 'notifications'
    model = Notification
    serializer_class = NotificationSerializer

    def get_object(self, **kwargs):
        logger.info('get_object: %s', kwargs)
        return self.model.objects.get(pk=kwargs['pk'])

    def get_query_set(self, **kwargs):
        logger.info('get_query_set: %s', kwargs)
        qs = self.model.objects.all()
        logger.info('%s', qs)
        return qs


route_handler.register(NotificationRouter)
