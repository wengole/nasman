from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wizfs.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

import configurations

configurations.setup()

app = Celery('wizfs')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
