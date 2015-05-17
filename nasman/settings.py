import sys
import os
from pathlib import Path

PROJ_DIR = Path(__file__).parent
ROOT_DIR = PROJ_DIR.parent
show_if_debug = lambda *x: DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'CHANGE THIS!!!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)
ALLOWED_HOSTS = []
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_if_debug
}
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel'
]

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
)
THIRD_PARTY_APPS = (
    'debug_toolbar',
    'bootstrap_pagination',
    'floppyforms',
    'sitetree',
    'django_extensions',
    'fontawesome',
    'rest_framework',
    'djangular',
)

PROJECT_APPS = (
    'nasman.snapshots',
    'nasman.core',
)

INSTALLED_APPS = PROJECT_APPS + DJANGO_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'djangular.middleware.DjangularUrlMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nasman.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'nasman.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'db',
        'NAME': 'nasman',
        'PASSWORD': 'nasman',
        'PORT': 5432,
        'TEST': {
            'CHARSET': None,
            'COLLATION': None,
            'MIRROR': None,
            'NAME': None
        },
        'TIME_ZONE': 'UTC',
        'USER': 'nasman'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = str(PROJ_DIR.joinpath('static'))

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

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
        },
        'DIRS': [str(PROJ_DIR.joinpath('templates')),],
    },
]
TEMPLATE_DIRS = (
    str(PROJ_DIR.joinpath('templates')),
)
BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['pickle', ]
CELERYD_PREFETCH_MULTIPLIER = 1
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(ROOT_DIR.joinpath('log', 'nasman.log')),
            'maxBytes': 10 * 1024 * 104,  # 10MB
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
        },
        'nasman': {
            'handlers': ['logfile'],
            'level': 'INFO',
        }
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SITETREE_MODEL_TREE_ITEM = 'snapshots.NasmanTreeItem'
