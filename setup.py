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
        'django-configurations',
        'dj_database_url',
    ]
)
