# -*- coding: utf-8 -*-
import os

from configurations import Configuration, values

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Common(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    SECRET_KEY = ('FftmF3EEwdCoJhqsCjpHUh2gPHXM83MhRTmnXDwyb8RbWxd5r4gXNwxM7eZ'
                  'nhJQP')
    DEBUG = True
    INTERNAL_IPS = ('127.0.0.1', '192.168.1.69',)
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []
    DJANGO_APPS = (
        'suit',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )
    THIRD_PARTY_APPS = (
        'crispy_forms',
        'menu',
        'haystack',
        'celery_haystack',
    )
    WIZFS_APPS = (
        'snapshots',
    )
    INSTALLED_APPS = WIZFS_APPS + DJANGO_APPS + THIRD_PARTY_APPS
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    ROOT_URLCONF = 'wizfs.urls'
    DATABASES = values.DatabaseURLValue(
        'postgres://wizfs:wizfs@127.0.0.1:5432/wizfs'
    )
    LANGUAGE_CODE = 'en-gb'
    TIME_ZONE = 'Europe/London'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
    )
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'xapian_backend.XapianEngine',
            'PATH': os.path.join(BASE_DIR, 'xapian_index'),
        },
    }
    HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'
    CELERY_HAYSTACK_MAX_RETRIES = 20
    CELERY_HAYSTACK_RETRY_DELAY = 2
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['pickle', ]
    CELERYD_PREFETCH_MULTIPLIER = 1
    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'logfile': {
                'level': 'INFO',
                'class': 'cloghandler.ConcurrentRotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'wizfs.log'),
                'maxBytes': 10*1024*104,  # 10MB
                'backupCount': 5,
                'formatter': 'default',
            }
        },
        'formatters': {
            'default': {
                'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['logfile'],
                'level': 'WARNING',
                'propagate': True,
            },
            'django': {
                'handlers': ['logfile'],
                'level': 'INFO',
            }
        }
    }
    SUIT_CONFIG = {
        'ADMIN_NAME': 'WiZFS',
    }
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"


class Local(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('debug_toolbar',)
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value(
        'django.core.mail.backends.console.EmailBackend'
    )
    DEFAULT_FROM_EMAIL = values.Value(
        'WiZFS <admin@exam.com>'
    )
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }


class Server(Common):
    DEBUG = False
    SECRET_KEY = values.SecretValue()
    EMAIL_HOST = values.Value('localhost')
    EMAIL_PORT = values.IntegerValue(25)
    EMAIL_HOST_USER = values.Value('')
    EMAIL_HOST_PASSWORD = values.Value('')
    EMAIL_SUBJECT_PREFIX = values.Value('[WiZFS] ')


class Travis(Common):
    DATABASES = values.DatabaseURLValue(
        'sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite3')
    )
    CELERY_HAYSTACK_DEFAULT_TASK = 'celery_haystack.tasks.CeleryHaystackSignalHandler'
    CELERY_ALWAYS_EAGER = True
    CELERY_HAYSTACK_TRANSACTION_SAFE = False
    CELERY_HAYSTACK_DEFAULT_ALIAS = None
    CELERY_HAYSTACK_MAX_RETRIES = 1
    CELERY_HAYSTACK_RETRY_DELAY = 1
