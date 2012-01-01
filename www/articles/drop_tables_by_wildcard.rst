=========================================
How to drop MySQL tables using a wildcard
=========================================

--------------------------------------------------------------------------------------
You can use awk with MySQL to drop tables that match a given pattern. :: Python,Django
--------------------------------------------------------------------------------------


Problem
=======
You want to drop all tables in a MySQL database that match some pattern.  It would be nice if the 
following worked

.. sourcecode:: mysql

    mysql> DROP TABLES LIKE 'order_%';

.. note:: 
   This is a special note

Solution
========
Use the following command

.. sourcecode:: bash

    $ mysql -D $DBNAME -e "SHOW TABLES LIKE 'order_%'" | \
      awk 'BEGIN {print "SET FOREIGN_KEY_CHECKS=0;"} 
           /^|/ {print "DROP TABLE " $1 ";"}' | \
      mysql -D $DBNAME

This uses awk to filter the results of the call to ``SHOW TABLES``, which does support the pattern
matching syntax.  

.. sourcecode:: html+django

    <ul>
        {% for user in users %}
            <li>{% include "_render_user.html" %}</li>
        {% endfor %}
    </ul>

Discussion
==========

The output of the ``SHOW TABLES`` call takes this form:

.. sourcecode:: bash

    $ mysql -D databasename -M -e "SHOW TABLES"
    +-----------------------------------+
    | order_billdeskrefund              |
    | order_billingaddress              |
    | order_communicationevent          |
    | order_line                        |
    | order_lineattribute               |
    | order_lineprice                   |
    | order_order                       |
    | order_orderdiscount               |
    | order_ordernote                   |
    | order_paymentevent                |
    | order_paymenteventquantity        |
    +-----------------------------------+

A similar command for showing table sizes is:

.. sourcecode:: bash

    $ mysql -D $DBNAME -N -e "SHOW TABLES" | \
      awk '/^|/ {print "SELECT COUNT(*) AS " $1 " FROM " $1 ";"}' | \
      mysql -D $DBNAME
