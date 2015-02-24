wizfs
=====

.. image:: https://travis-ci.org/wengole/wizfs.svg?branch=master
    :target: https://travis-ci.org/wengole/wizfs

A Django based ZFS management interface.

Installation
------------

This project uses buildout. Clone the project then from inside the project
directory

.. code-block::

   virtualenv -p /usr/bin/python2 .
   . bin/activate
   python bootstrap.py
   bin/buildout

Ensure you buildout from within the virtualenv. 
Especially if your system python isn't python2, 
otherwise Xapian Bindings will not compiles

As this makes use of a ZFS library,
it either needs to be run as root (dangerous) or
you need to allow ``/dev/zfs`` to be run as non-root
See `this issue on github <https://github.com/zfsonlinux/zfs/issues/362>`_.

The traditional manage.py gets put into bin/

.. code-block::

   bin/manage runserver

