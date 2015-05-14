import logging

from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter

from .models import Notification
from .serializers import NotificationSerializer

logger = logging.getLogger(__name__)


class NotificationRouter(ModelRouter):
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

    def get_count(self):
        logger.info('Getting count for user: %s', self.connection.user)
        return self.get_query_set().count()



route_handler.register(NotificationRouter)
