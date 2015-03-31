Installation
============

Before building out the project,
first make sure the prerequisite system packages are installed

As this makes use of a ZFS library,
it either needs to be run as root (dangerous) or
you need to allow ``/dev/zfs`` to be accessed by non-root users

See `this issue on github <https://github.com/zfsonlinux/zfs/issues/362>`_.

Prerequisites
-------------

 * ZFS
 * SPL
 * PostgreSQL
 * Redis

Other dependencies
------------------

These are installed by buildout

 * Xapian (search backend)
 * Celery (task queue)

Xapian requires no further input from the user.
Celery however should be configured to run as a service.
This is left as an exercise to the user :) (for now)

.. todo::

    * Document how to set up Celery as a service (systemd, supervisor)

Buildout
--------

This project uses buildout. Clone the project then from inside the project
directory

.. code-block:: bash

   virtualenv -p /usr/bin/python2 .
   . bin/activate
   python bootstrap.py
   deactivate
   bin/buildout

The traditional manage.py gets put into bin/

.. code-block:: bash

   bin/manage runserver


Database Initialisation
-----------------------

.. code-block:: bash

    su postgres
    createuser wizfs --interactive
    createdb -U wizfs wizfs
    psql
    psql> alter role wizfs unencrypted password '{your password here}';

Don't for get to update the settings.py with your database password
