==============================================
How to install PostGIS and GeoDjango on Ubuntu
==============================================
--------------------------------------
Another note-to-self :: django, python 
--------------------------------------

Despite its `extensive documentation`_, getting GeoDjango installed and configured
can be a pain.  Here are my notes for future reference:

.. _`extensive documentation`: https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/

Installation on Ubuntu 12.04
----------------------------

First, ensure your system locale is UTF8 as PostgreSQL uses it to determine its
default encoding during installation:

.. sourcecode:: bash

    $ export LANGUAGE="en_US.UTF-8"
    $ export LANG="en_US.UTF-8"
    $ export LC_ALL="en_US.UTF-8"

Now install dependencies:

.. sourcecode:: bash

    $ sudo apt-get update
    $ sudo apt-get install postgresql-server-dev-9.1 postgresql-9.1-postgis 

PostgreSQL should now be installed and running with UTF8 encodings.  Verify this
with:

.. sourcecode:: bash

    $ sudo -u postgres psql -l    
                                         List of databases
           Name       |  Owner   | Encoding |   Collate   |    Ctype    |
    ------------------+----------+----------+-------------+-------------+-...
     postgres         | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
     template0        | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
                      |          |          |             |             |
     template1        | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
                      |          |          |             |             |

Now create a spatial database.  The above commands will have installed
PostGIS 1.5.3 hence, `according to Django's docs`_, we need to download and
install a shell script that executes the appropriate commands:

.. sourcecode:: bash

   $ wget https://docs.djangoproject.com/en/dev/_downloads/create_template_postgis-1.5.sh
   $ chmod +x create_template_postgis-1.5.sh

.. _`according to Django's docs`: https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/#creating-a-spatial-database-template-for-earlier-versions

and run it as a privileged user:

.. sourcecode:: bash

   $ sudo -u postgres ./create_template_postgis-1.5.sh

If this is successful, a deluge of SQL output will echo to the console.  This is
normal.   PostGIS is now correctly installed and we have a template database we
can use to create a database for our GeoDjango project.

.. sourcecode:: bash

   $ sudo -u postgres psql
   psql (9.1.9)
   Type "help" for help.
   
   postgres=# CREATE DATABASE sample_db TEMPLATE template_postgis;
   CREATE DATABASE
   postgres=# CREATE ROLE sameple_role WITH PASSWORD 'sample_password' LOGIN;
   CREATE ROLE

This is the tricky bit over: you can now ``pip install psycopg2`` and you're
basically done.

Common errors
=============

If your system locale is not UTF8 when attempting to create a spatial database,
you'll see something like this:

.. sourcecode:: bash

    $ sudo -u postgres ./create_template_postgis-debian.sh
    createdb: database creation failed: ERROR: encoding UTF8 does not match locale en_US
    DETAIL:  The chosen LC_CTYPE setting requires encoding LATIN1 
    FATAL:  database "template_postgis" does not exist

If PostgreSQL is not installed when trying to install psycopg2, you see
something that ends with this:

.. sourcecode:: bash

    warning: manifest_maker: standard file '-c' not found

    Error: pg_config executable not found.

    Please add the directory containing pg_config to the PATH
    or specify the full executable path with the option:

        python setup.py build_ext --pg-config /path/to/pg_config build ...

    or with the pg_config option in 'setup.cfg'.

I'll add more error symptoms when I see them in the wild.
