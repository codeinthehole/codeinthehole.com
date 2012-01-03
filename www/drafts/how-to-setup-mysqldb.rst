========================================
How to set-up MySQL for Python on Ubuntu
========================================

This is just for my own reference.

Starting with a vanilla Ubuntu install (tested with Hardy 10.04):

.. sourcecode:: bash

    apt-get install build-essential python-dev mysql-server

then (assuming you have ``pip`` installed):

.. sourcecode:: bash

    pip install MySQL-python