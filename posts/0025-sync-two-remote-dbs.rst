=======================================================
How to sync a MySQL table between two remote databases.
=======================================================
--------------------------------------
Trickier than you might think :: mysql
--------------------------------------

Definitely tricker than you might think.

Seems like it should be trivial using ``SELECT ... INTO OUTFILE`` and ``LOAD DATA
INFILE ...`` to make the transfer via dumping the table into a temporary file.
However, ``SELECT ... INTO OUTFILE`` creates a file on the remote server
rather than locally. This prevents the use of ``LOAD DATA INFILE`` for the second
step as the file being loaded has to be local or on the destination server.

Following the `guidance in the docs`_, you can create local dump of a table by
using the ``--execute`` option to output the results of a ``SELECT ...`` statement
into a local file.

.. _`guidance in the docs`: http://dev.mysql.com/doc/refman/5.0/en/select.html

.. sourcecode:: bash

    mysql -D database_name -e "SELECT ... " > /path/to/file.txt

This works but has two downsides:

* First, running a shell command forces you to step outside the MySQL adapter of
  your progamming language which means it is a new place where the database
  credentials need to be passed. Shelling out commands always feels like you've
  failed.

* Further, as far as I can tell, you can't control the field separator or line
  endings using this technique (in the same way as you can with ``SELECT ... INTO
  OUTFILE ...``) and so the file includes an unwanted line with the field names
  and tab-separates the fields.

It's worth noting the ``mysqldump`` isn't much help here, as the ``--tab`` option
that allows CSV output to be generated only works with a local database
connection.

Now that we've got our data locally, we load it into the remote database using
``LOAD DATA INFILE`` and make use of the ``LOCAL`` keyword which lets us use a
local data file:

.. sourcecode:: bash

    mysql -h x.x.x.x -u user -D database_name --password=... -e \
    "LOAD DATA LOCAL INFILE '/path/to/file.txt' \
    REPLACE INTO TABLE table_name \
    IGNORE 1 LINES"

Of course, you may want to truncate the table first if you want a clean sync.
As this operations locks the destination table, it often makes sense to load
the data into a temporary copy of the table, and then perform a ``RENAME TABLE``
operation to swap in the new table.

Here's a quick and dirty PHP implementation:

.. sourcecode:: php

    $tableName = 'some_table';
    $sql =
       "SELECT * 
        FROM $tableName";
    $pathToCsv = '/tmp/some-file.csv';
    $command = sprintf("mysql -h %s -u %s  --password=%s -D %s -e '%s' > %s",
        '10.0.0.2', 
        'db-user', 
        'db-password', 
        'database_name', 
        $sql, 
        $pathToCsv);
    exec($command);

    $sql =
       "LOAD DATA LOCAL INFILE '$pathToCsv'
        REPLACE INTO TABLE `$tableName`
        CHARACTER SET 'utf8'
        IGNORE 1 LINES";
    $db->execute($sql); // Using your favourite database adapter