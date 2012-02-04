==============================================================
Solving MySQL connection problems caused by a dead name server
==============================================================
-------------------------------------------------------
MySQL's DNS lookups can cause serious problems :: mysql
-------------------------------------------------------


A client site went down today.  This is what happened and how it was fixed.  

Symptoms
--------

The immediate symptom is that your application servers can't connect to your
database servers.  Attempted connections get an error message:

    Can't connect to MySQL server on '10.10.110.11' (111)

The relevant MySQL process list reveals a long list of attempted connections in
state ``login``:

.. sourcecode:: bash

    root@server-db1:~ $ mysqladmin processlist
    +-----+----------------------+--------------------+----+---------+------+-------+
    | Id  | User                 | Host               | db | Command | Time | State |
    +-----+----------------------+--------------------+----+---------+------+-------+
    ...
    | 261 | unauthenticated user | 10.20.115.19:43381 |    | Connect |      | login |
    | 262 | unauthenticated user | 10.20.115.19:43396 |    | Connect |      | login |
    | 263 | unauthenticated user | 10.20.115.19:43420 |    | Connect |      | login |
    | 264 | unauthenticated user | 10.20.115.19:43429 |    | Connect |      | login |
    | 265 | unauthenticated user | 10.20.115.4:55297  |    | Connect |      | login |
    ...

Your site is probably down as no request can connect to the database - people 
are starting to get upset.

Problem
-------

When a client connects to MySQL, the newly spawned thread attempts to resolve the host name (see 
`MySQL's documentation on DNS`_).
This problem is caused by the first name server in ``/etc/resolv.conf`` being down, causing the
DNS request to time-out.  Hence, every connection to MySQL sits for a minute waiting for the 
timeout to occur.  Within a few seconds, no client will be able to connect.

.. _`MySQL's documentation on DNS`: http://dev.mysql.com/doc/refman/5.0/en/dns.html

You can verify this using the ``dig`` command to exercise the name servers in ``/etc/resolv.conf``.
Here's the broken one (you'll have to wait for the time-out):

.. sourcecode:: bash

    dig @180.179.39.80 www.google.com

    ; <<>> DiG 9.7.0-P1 <<>> @180.179.39.80 www.google.com
    ; (1 server found)
    ;; global options: +cmd
    ;; connection timed out; no servers could be reached

A working name server would return something like:

.. sourcecode:: bash

    dig @180.179.39.81 www.google.com

    ; <<>> DiG 9.7.0-P1 <<>> @180.179.39.81 www.google.com
    ; (1 server found)
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 14538
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 6, AUTHORITY: 4, ADDITIONAL: 4

    ;; QUESTION SECTION:
    ;www.google.com.googleINA

    ;; ANSWER SECTION:
    www.google.com.com      427763  IN  CNAME   www.l.google.com.
    www.l.google.com.com    97      IN  A       74.125.236.116
    www.l.google.com.com    97      IN  A       74.125.236.112
    www.l.google.com.com    97      IN  A       74.125.236.113
    www.l.google.com.com    97      IN  A       74.125.236.114
    www.l.google.com.com    97      IN  A       74.125.236.115

    ;; AUTHORITY SECTION:
    google.com.com          250791  IN  NS      ns2.google.com.
    google.com.com          250791  IN  NS      ns3.google.com.
    google.com.com          250791  IN  NS      ns4.google.com.
    google.com.com          250791  IN  NS      ns1.google.com.

    ;; ADDITIONAL SECTION:
    ns1.google.com.com      76667   IN  A       216.239.32.10
    ns1.google.com.com      76667   IN  A       216.239.34.10
    ns1.google.com.com      76667   IN  A       216.239.36.10
    ns1.google.com.com      76667   IN  A       216.239.38.10

    ;; Query time: 13 msec
    ;; SERVER: 180.179.39.81#53(180.179.39.81)
    ;; WHEN: Thu Feb  2 16:18:38 2012
    ;; MSG SIZE  rcvd: 268

Solution
--------

The root solution is to fix the name server, but sometimes that isn't in your control.  

You can work around the borked name server by restarting MySQL with the
``--skip-name-resolve`` option.  This prevents MySQL trying to resolve the host
name for each thread, bypassing the name server problem.

Alternatively, you can remove the broken DNS server from your
``/etc/resolv.conf``.

Discussion
----------

Note that running MySQL with ``--skip-name-resolve`` means you can't use
hostnames in your privileges table.  Thus, you may have to reconfigure your
client users to get your site back up.  You can verify this by using the
following SQL to inspect your configured users and hosts:

.. sourcecode:: sql

    mysql> SELECT user, host FROM mysql.user;

Check to see if the ``host`` column uses domain names.

Credits
-------

Thanks to Tangent's operations team `@timbobsteve`_ and `@kuramanga`_ for their help 
in debugging and fixing this.

.. _`@timbobsteve`: https://twitter.com/#!/timbobsteve
.. _`@kuramanga`: https://twitter.com/#!/kuramanga
