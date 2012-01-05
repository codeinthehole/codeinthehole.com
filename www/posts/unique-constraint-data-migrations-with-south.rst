=====================================
Using South to add unique constraints
=====================================


Problem
=======
You want to add a unique database index on a Django model field, but the database already has duplicate values
for this field which need to be cleaned up.

Solution
========
Use a South migration with some custom code to clean up the duplicate rows.  

Start by adding ``unique=True`` to the field in question and generate the standard schema migration to 
run the appropriate ``ALTER TABLE`` SQL:

.. sourcecode:: bash

    ./manage.py schemamigration myapp --auto

Now edit this file to handle the data clean-up:

.. sourcecode:: python

    class Migration(SchemaMigration):
        
        def forwards(self, orm):
            self.clean_dupes(orm)

        def clean_dupes(self, orm):
            sql = """SELECT GROUP_CONCAT(id ORDER BY id SEPARATOR ',') AS ids,
                            COUNT(*) AS freq
                     FROM myapp.table
                     GROUP BY field
                     HAVING freq  > 1"""
            for id_str,_ in db.execute(sql):
                ids = id_str.split(

                

Discussion
==========
You could have the clean-up as a separate data migration, but my experience is that the schema
migration is already committed by someone who didn't have these data issues in their local DB
and failed to consider the case.
