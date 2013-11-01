========================================
Dumping and restoring a PostGIS database
========================================
-----------------------------------------------
Harder than it should be :: postgres, geodjango
-----------------------------------------------

I wasted at least twenty minutes getting this to work.  These are my notes.

Problem
-------

You are using a PostGIS database and want to take a backup copy from production
and restore it in a different environment.  One complication is that
each environment connects to its database with its own user.

This is a common scenario if you are using GeoDjango_.

.. _GeoDjango: https://docs.djangoproject.com/en/dev/ref/contrib/gis/

Solution
--------

Suppose your production database is called "myproject_prod" which you connect to
with user "myproject_prod_role" and you want to replace your existing stage
database "myproject_stage" that you connect to with user "myproject_stage_role".

First, dump your production database:

.. sourcecode:: bash

    $ pg_dump --no-acl --no-owner $DATABASE > dump.sql

where:

* access control is ignored (``--no-acl``) as your production database may have additional users
  that you're not interested in;

* ownership is ignored (``--no-owner``) as you will be restoring as a different user.

Now, copy the SQL file across to the appropriate server and create the
destination database from a PostGIS template with the appropriate owner:

.. sourcecode:: postgres

    postgres=# DROP DATABASE myproject_stage;
    postgres=# CREATE DATABASE myproject_stage TEMPLATE template_postgis OWNER myproject_role_stage;

and restore the database using the stage user:

.. sourcecode:: bash

    $ psql --host=127.0.0.1 --username=myproject_role_stage myproject_stage < dump.sql

Be warned: this command will generated a lot of warnings (which can be ignored).
This happens as ``pg_dump`` generates SQL relative to the 'template0' database
(not 'template_postgis' which would be more helpful in this situation).  Thus,
the dumped SQL file contains the definitions of PostGIS types which have already
been defined when we created the database from "template_postgis".  

.. note::

    The host is specified in the restore operation (``--host=127.0.0.1``) so as
    to trigger the correct authentication rules from ``pg_hba.conf``.  I usually
    forget this and am confused about why I can't authenticate.  You might not
    need this if your authentication config is different.

Related reading:

- `Backup and Restore of a PostGis database`_ - a relevant thread from the
  PostGIS mailing list.
  
.. _`Backup and Restore of a PostGis database`: http://postgis.17.x6.nabble.com/Backup-and-Restore-of-a-PostGis-database-td3565498.html
