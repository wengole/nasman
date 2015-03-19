import os

import gevent.socket
import redis.connection
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer

redis.connection.socket = gevent.socket
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wizfs.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')
application = uWSGIWebsocketServer()
