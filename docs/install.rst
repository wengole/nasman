Installation
============

NASMan is a `Docker <https://www.docker.com>`_ application.
To install it you will need to have docker and docker-compose installed on your host system

NASMan requires access to ZFS in order to be useful.
The main docker container runs in privileged_ mode.
This allows the container and the app to access the ZFS filesystems on the host

.. _privileged: https://docs.docker.com/reference/run/#runtime-privilege-linux-capabilities-and-lxc-configuration

Prerequisites
-------------

 * Docker
 * Docker compose
 * ZFS (for now, will make this optional later)

Installation
------------

Clone the project, then from inside the project directory

.. code-block:: bash

   $ docker-compose up -d
   $ docker exec nasman_web_1 python manage.py migrate
   $ docker exec nasman_web_1 python manage.py sitetree_resync_apps

Your installation will now be running and listening on port 8000 of the host.

At the moment it is using the Django runserver,
which is discouraged from being used in production for performance issues,
however due to the use case of NASMan,
it seems unlikely to be an issue.
Feel free to raise an issue on github of you encounter any problems.
