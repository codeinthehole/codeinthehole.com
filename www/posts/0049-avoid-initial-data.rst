======================================
Prefer data migrations to initial data
======================================
-------------------------------------------------
South provides a better way :: django, deployment
-------------------------------------------------

Django provides several mechanisms for `loading initial data for models`_, such
as leveraging JSON fixtures or files of raw SQL - James Bennett offers a
`good overview`_.

.. _`loading initial data for models`: https://docs.djangoproject.com/en/dev/howto/initial-data/
.. _`good overview`: http://www.b-list.org/weblog/2007/nov/21/install-time/

Each documented method involves initialising data as part of the syncdb event, either by
loading a fixture file or by hooking into the syncdb signal.  However, there is a
serious pitfall with these techniques, as described in the `Django docs`_:

.. _`Django docs`: https://docs.djangoproject.com/en/dev/howto/initial-data/#automatically-loading-initial-data-fixtures

    This is extremely convenient, but be careful: remember that the data will be
    refreshed every time you run syncdb. So don't use initial_data for data
    you'll want to edit.

Storing data in a database that you don't want to edit seems like an
anti-pattern to me.  If it never changes, a database probably isn't the right
place to store it.

That aside, there are certainly times when you want to seed a new database with
data that can be edited.  In these circumstances, the documented methods fall
down as you can accidentally clobber live data if you run syncdb again.

You might argue that you should only run syncdb once but in my experience, it is
useful to run syncdb as part of your deployment script so that any newly added
apps have their tables created automatically.  

South data migrations
---------------------

A better way to provide initial data is to use the database migration library
`South`_ to create `data migrations`_.  The advantages are:

.. _`South`: http://south.aeracode.org/docs/index.html
.. _`data migrations`: http://south.aeracode.org/docs/tutorial/part3.html

* Data migrations will only run once and so they won't clobber any data.
* They will run automatically in all environments - no manual deployment steps
  required.

The only disadvantage is that you need to use South, which most sensible
Django projects already do.

Simple example
--------------

Create a blank data migration:

.. sourcecode:: bash

    ./manage.py datamigration myapp mymigrationname

then implement the ``forward`` method to create the appropriate initial data:

.. sourcecode:: python

    def forwards(self, orm):
        from myapp.models import Frob
        for name in ('Foo', 'Bar'):
            Frob.objects.create(name=name)

See the `worked example`_ in South's docs for further details on writing data migrations.

.. _`worked example`: http://south.aeracode.org/docs/tutorial/part3.html

Using fixture files
-------------------

It's possible to use JSON fixture files with data migrations, by utilising
the ``call_command`` function.  

.. sourcecode:: python

    def forwards(self, orm):
        from django.core.management import call_command
        call_command('loaddata', 'countries.json')

This is a very useful feature as you can use the ``dumpdata`` command to produce your
initial fixtures, and you will have them available to be used by unit tests.
