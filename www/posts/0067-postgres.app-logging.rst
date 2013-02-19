====================================
Configuring logging for Postgres.app
====================================
---------------------------------------------------------
The recommended way of debugging SQL problems :: postgres
---------------------------------------------------------

Problem
-------

You're using Postgres.app_ on a Mac for local development but are getting SQL
errors from your application.  You're seeing an error message:

.. sourcecode:: bash

    ERROR:  current transaction is aborted, commands ignored until end of
    transaction block

.. _Postgres.app: http://postgresapp.com/

This isn't very useful: you want to know which query is generating the error.

Solution
--------

Turn on Postgres' logging and watch the log files when the error is generated.   

This is done by editing ``~/Library/Application Support/Postgres/var/postgresql.conf`` and setting:

.. sourcecode:: conf

    logging_collector = on
    log_directory = 'pg_log'

then restarting Postgres to pick up the new settings.  You can then watch the
log files to find out which queries are failing:

.. sourcecode:: bash

    $ tail -f ~/Library/Application\ Support/Postgres/var/pg_log/*

Discussion
----------

By default, Postgres.app does not have logging enabled which makes local
debugging difficult.  
