================
Monitoring MySQL
================
--------------------------------------------------------
``watch`` ing ``mysqladmin`` ftw :: mysql, commandlinefu
--------------------------------------------------------

Just a quick tip on monitoring the queries that mysql is handling on a
production site. You can use the mysqladmin tool to return a list of the
processes currently being handled. Combining this with the UNIX watch command
allows a real-time monitoring of what's going on.

.. sourcecode:: bash

    watch -n 1 mysqladmin processlist

The ``-n 1`` specifies that mysqladmin executes every second. Depending on your
set-up, you may need to specify a mysql user and password:

.. sourcecode:: bash

    watch -n 1 mysqladmin --user=<user> --password=<password> processlist