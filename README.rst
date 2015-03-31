WiZFS - A Django ZFS management tool
====================================

.. image:: https://travis-ci.org/wengole/wizfs.svg?branch=master
   :target: https://travis-ci.org/wengole/wizfs
   :alt: Continuous Integration Status
.. image:: https://coveralls.io/repos/wengole/wizfs/badge.svg?branch=develop
   :target: https://coveralls.io/r/wengole/wizfs?branch=develop
   :alt: Coverage Status
.. image:: https://readthedocs.org/projects/wizfs/badge/?version=latest
   :target: https://readthedocs.org/projects/wizfs/?badge=latest
   :alt: Documentation Status

A Django based ZFS management interface.

Installation
------------

This project uses buildout. Clone the project then from inside the project
directory

.. code-block:: bash

   virtualenv -p /usr/bin/python2 .
   . bin/activate
   python bootstrap.py
   deactivate
   bin/buildout

As this makes use of a ZFS library,
it either needs to be run as root (dangerous) or
you need to allow ``/dev/zfs`` to be accessed by non-root users
See `this issue on github <https://github.com/zfsonlinux/zfs/issues/362>`_.

The traditional manage.py gets put into bin/

.. code-block:: bash

   bin/manage runserver

