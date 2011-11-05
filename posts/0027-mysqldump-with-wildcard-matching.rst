======================================
mysqldump with wildcard table matching
======================================
---------------------------------------------------------
Using the fu to enhance mysqldump :: mysql, commandlinefu
---------------------------------------------------------

Ever wanted to use ``mysqldump`` to dump tables that match a wildcard pattern? I
have. It's not currently supported as an option but can be achieved with a
little bash magic. Here's how:

.. sourcecode:: bash

    #!/bin/bash
    if [ $# -lt 2 ]
    then
        echo "Usage: `basename $0` database wildcardpattern"
        echo "Eg: `basename $0` mydatabase App_%"
        exit 1
    fi
    database=$1
    pattern=$2
    mysqldump $database `mysql -ND $database -e "SHOW TABLES LIKE '$pattern'" | awk '{printf $1" "}'`

This uses a simple SQL query to extract all the table names that match the
pattern and concatenate them in the format that mysqldump expects. Note that
you'll need your ``~/.my.cnf`` set up correctly to allow the connections to MySQL
to happen without a authentication prompt.