import os

BASE_DIR = os.path.dirname(__file__)
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
    'debug_toolbar',
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
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                         'HOST': '127.0.0.1',
                         'NAME': 'wizfs',
                         'PASSWORD': u'wizfs',
                         'PORT': 5432,
                         'TEST': {'CHARSET': None,
                                  'COLLATION': None,
                                  'MIRROR': None,
                                  'NAME': None},
                         'TIME_ZONE': 'UTC',
                         'USER': 'wizfs'}}
