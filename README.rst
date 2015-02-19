wizfs
=====

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

The traditional manage.py gets put into bin/

.. code-block::

   bin/manage runserver
