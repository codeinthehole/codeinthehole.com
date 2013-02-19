==========================================
Altering Postgres table columns with South
==========================================
-----------------------------------------------------
Using ``USING`` to cast correctly :: postgres, django
-----------------------------------------------------

Problem
-------

You're using Postgres with Django.  

You change a field type of one of your models, generate an ``--auto`` South migration and
attempt to run it.  However, South chokes on the new migration complaining that
the data in the column cannot be cast to the new type.

For instance, I recently changed a ``CharField`` to a ``TimeField``.  The
corresponding migration lead to an error:

.. sourcecode:: console

    Running migrations for stores:
    - Migrating forwards to 0009_auto__chg_field_openingperiod_start__chg_field_openingperiod_end.
    > stores:0008_auto__del_unique_store_slug
    > stores:0009_auto__chg_field_openingperiod_start__chg_field_openingperiod_end
    FATAL ERROR - The following SQL query failed: ALTER TABLE "stores_openingperiod" ALTER COLUMN "start" TYPE time, ALTER COLUMN "start" DROP NOT NULL, ALTER COLUMN "start" DROP DEFAULT;
    The error was: column "start" cannot be cast to type time without time zone

Solution
--------

Write the ``ALTER TABLE`` SQL by hand making use of the ``USING`` clause to
specify how to compute the new value from the old.

For the above example, the correct SQL to use is:

.. sourcecode:: sql

    ALTER TABLE "stores_openingperiod" 
        ALTER COLUMN "end" DROP DEFAULT, 
        ALTER COLUMN "end" DROP NOT NULL, 
        ALTER COLUMN "end" TYPE time USING timestamp with time zone 'epoch'

We need to modify the migration file to execute raw SQL with ``db.execute``
instead of using ``db.alter_table`` to generate the SQL.  So we change:

.. sourcecode:: python

    db.alter_column('stores_openingperiod', 'end', self.gf('django.db.models.fields.TimeField')(null=True))

to:

.. sourcecode:: python

    db.execute(
        'ALTER TABLE "stores_openingperiod" '
        'ALTER COLUMN "end" DROP DEFAULT, '
        'ALTER COLUMN "end" DROP NOT NULL, '
        'ALTER COLUMN "end" TYPE time USING timestamp with time zone \'epoch\''
    )

and all is well.

A similar technique can be used wherever Postgres refuses to run a migration due
to casting issues.  See the `Postgres documentation`_ for more examples of the
``USING`` clause.

.. _`Postgres documentation`: http://www.postgresql.org/docs/9.1/static/sql-altertable.html
