Installation
============

Before building out the project,
first make sure the prerequisite system packages are installed

If you're using ZFS,
you either need to run NASMan as root (dangerous) or
you need to allow ``/dev/zfs`` to be accessed by non-root users

See `this issue on github <https://github.com/zfsonlinux/zfs/issues/362>`_.

.. todo::

    * Figure out what if anything needs to be done for BTRFS

Prerequisites
-------------

 * Python 3.3+
 * PostgreSQL
 * Redis

Other dependencies
------------------

These are installed by buildout

 * Celery (task queue)

Celery should be configured to run as a service.
This is left as an exercise to the user :) (for now)

.. todo::

    * Document how to set up Celery as a service (systemd, supervisor)

Installation
------------

Clone the project, then from inside the project directory

.. code-block:: bash

   virtualenv -p /usr/bin/python2 .
   bin/pip install cffi
   bin/pip install -r requirements/local.txt

Run ``mange.py`` with the virtualenv interpreter

.. code-block:: bash

   bin/python manage.py runserver


Database Initialisation
-----------------------

.. code-block:: bash

    su postgres
    createuser nasmannasman --interactive
    createdb -U nasman nasman
    psql
    psql> alter role nasman unencrypted password '{your password here}';

Don't for get to update the settings.py with your database password.

Then run the migrations:

.. code-block:: bash

    bin/python manage.py migrate
