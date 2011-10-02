=========================
Checking all MySQL tables
=========================
------------------------------------------------------------------------------------
Using the commandline to build a string of ``CHECK`` commands : commandlinefu, mysql
------------------------------------------------------------------------------------

It's well known that MyISAM tables are prone to corruption and need to be
regularly checked and repaired. Moreover, in a production environment, it can
be beneficial to run a daily check of all tables and mail news of any errors to
an appropriate developer/DBA.

There are two options for checking MySQL tables. The most effective method is
to run the `myisamchk utility`__ directly on the index files (``.MYI``) of the tables
in question (some simple shell expansion makes this easy):

__ http://dev.mysql.com/doc/refman/5.0/en/myisamchk.html

.. sourcecode:: bash

    myisamchk --silent --fast /path/to/datadir/*/*.MYI

However, this proses a problem in that you must ensure that no other programs
are accessing the tables while they are being checked. Hence they must be
locked, or better still, the MySQL daemon stopped before running any checks.
Perversely, if this is not done, the act of checking the tables can corrupt
them.

Another option is to use the ``CHECK TABLE`` syntax in SQL (which does not pose a
risk of corruption). There are various scripts (written in PHP and bash) posted
on the ``CHECK TABLE`` `manual page`_ but this operation can be done easily through a
single line:

.. _manual page: http://dev.mysql.com/doc/mysql/en/CHECK_TABLE.html

.. sourcecode:: bash

    mysql -p<password> -D<database> -B -e "SHOW TABLES" \
    | awk '{print "CHECK TABLE "$1";"}' \
    | mysql -p<password> -D<database>

This dynamically creates a list of ``CHECK TABLE ...`` commands which is piped
into MySQL for execution.

For checking a selection of tables rather than all, use the LIKE operator when
selecting the tables to check:

.. sourcecode:: bash

    mysql -p<password> -D<database> -B -e "SHOW TABLES LIKE 'User%'" \
    | awk 'NR != 1 {print "CHECK TABLE "$1";"}' \
    | mysql -p<password> -D<database>

This only checks the tables that start 'User'. Note that the awk program has an
extra clause to ensure that the first line of MySQL output is skipped.
