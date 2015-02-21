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
        'dj_database_url',
        'pyzfscore',
        'django-haystack',
        'xapian-haystack',
        'cffi',
    ],
    dependency_links=[
        'https://github.com/akatrevorjay/pyzfscore/tarball/master#egg=pyzfscore-0.0.1',
        'https://github.com/notanumber/xapian-haystack/tarball/master#egg=xapian-haystack-1.1.6b0',
    ]
)

