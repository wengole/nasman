# -*- coding: utf-8 -*-
import os
import sys

from configurations import Configuration, values


BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE_DIR, 'wizfs'))


class Common(Configuration):
    BASE_DIR = BASE_DIR
    SECRET_KEY = ('FftmF3EEwdCoJhqsCjpHUh2gPHXM83MhRTmnXDwyb8RbWxd5r4gXNwxM7eZ'
                  'nhJQP')
    DEBUG = True
    INTERNAL_IPS = ('127.0.0.1', )
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []
    DJANGO_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.humanize',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
    )
    THIRD_PARTY_APPS = (
        'bootstrap_pagination',
        'floppyforms',
        'menu',
    )
    WIZFS_APPS = (
        'snapshots',
    )
    INSTALLED_APPS = WIZFS_APPS + DJANGO_APPS + THIRD_PARTY_APPS
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    )
    ROOT_URLCONF = 'urls'
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
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'assets'),
    )
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': (
                    'django.contrib.auth.context_processors.auth',
                    'django.core.context_processors.debug',
                    'django.core.context_processors.i18n',
                    'django.core.context_processors.media',
                    'django.core.context_processors.static',
                    'django.core.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    'django.core.context_processors.request',
                )
            }
        },
    ]
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['pickle', ]
    CELERYD_PREFETCH_MULTIPLIER = 1
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'logfile': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
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
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'


class Local(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('debug_toolbar',)
    EMAIL_HOST = 'localhost'
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
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.versions.VersionsPanel',
    ]


class Server(Common):
    DEBUG = False
    SECRET_KEY = values.SecretValue()
    EMAIL_HOST = values.Value('localhost')
    EMAIL_PORT = values.IntegerValue(25)
    EMAIL_HOST_USER = values.Value('')
    EMAIL_HOST_PASSWORD = values.Value('')
    EMAIL_SUBJECT_PREFIX = values.Value('[WiZFS] ')


class Test(Common):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/2',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }


class Travis(Test):
    DATABASES = values.DatabaseURLValue(
        'postgres://postgres@127.0.0.1:5432/travis_ci_test'
    )
    CELERY_ALWAYS_EAGER = True
