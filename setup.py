from distutils.core import setup

setup(
    name='wizfs',
    version='0.1.0',
    packages=['wizfs',],
    package_dir={'': 'src'},
    url='https://github.com/wengole/wizfs',
    license='BSD',
    author='Ben Cole',
    author_email='wengole@gmail.com',
    description='A Django based ZFS management interface.',
    install_requires=[
        'Django',
        'django-simple-menu',
        'django-crispy-forms',
        'django-debug-toolbar',
        'django-suit',
        'django-configurations',
        'dj_database_url',
        'ConcurrentLogHandler',
        'pyzfscore',
        'django-haystack',
        'xapian-haystack',
        'cffi',
        'mock',
        'python-dateutil',
        'ipython',
        'pytz',
        'python-magic',
        'Celery[redis]',
        'eventlet',
        'flower',
        'pyinotify',
    ],
    dependency_links=[
        'https://github.com/akatrevorjay/pyzfscore/tarball/master#egg=pyzfscore-0.0.1',
        'https://github.com/notanumber/xapian-haystack/tarball/master#egg=xapian-haystack-1.1.6b0',
        'https://github.com/mher/flower/tarball/master#egg=flower-0.7.4',
        'https://github.com/jezdez/django-configurations/tarball/master#egg=django-configurations-0.9.0',
        'https://github.com/django-haystack/django-haystack/tarball/v2.4.0#egg=django-haystack-2.4.0',
    ]
)

