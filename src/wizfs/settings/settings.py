"""
Django settings for wizfs project.
"""
import os

from configurations import Configuration, values


class Common(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    SECRET_KEY = ('FftmF3EEwdCoJhqsCjpHUh2gPHXM83MhRTmnXDwyb8RbWxd5r4gXNwxM7eZ'
                  'nhJQP')
    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []
    DJANGO_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )
    THIRD_PARTY_APPS = (
        'debug_toolbar',
        'crispy_forms',
        'menu',
    )
    WIZFS_APPS = (
        'base',
        'snapshots',
    )
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + WIZFS_APPS
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    ROOT_URLCONF = 'wizfs.urls'
    WSGI_APPLICATION = 'wizfs.wsgi.application'
    DATABASES = values.DatabaseURLValue(
        'sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite3'),
        environ=True
    )
    LANGUAGE_CODE = 'en-gb'
    TIME_ZONE = 'Europe/London'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    STATIC_URL = '/static/'
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


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    pass


class Productionk(Common):
    """
    The in-production settings.
    """
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG

    SECRET_KEY = values.SecretValue()