===========================================
Running django cronjobs within a virtualenv
===========================================
--------------------------------
Use the source :: python, django
--------------------------------

If you use virtual environments on your django servers, then getting manage.py
commands to run from cron is a little tricky. You need to activate the
virtualenv before running the command and so you might think that the following
would work:

.. sourcecode:: bash

    */10 * * * * root source /var/www/mysite/virtualenvs/dev/bin/activate && /var/www/mysite/build/dev/manage.py some_custom_command > /dev/null

It doesn't, although it's tricky to spot why as ``/var/log/syslog`` doesn't give
much away (Debian-specific of course).

A good trick for cronjob debugging is to alias yourself as root within
``/etc/aliases``:

.. sourcecode:: bash

    postmaster: root
    root: yourusername@gmail.com

and run ``sendmail -bi`` to initialise the aliases. As errors from cronjobs are
emailed to root, you will also get a copy. Doing this reveals the above cron
file fails as the default shell for cron is ``/bin/sh`` which doesn't support the
source command.

The solution is to set the $SHELL variable within the cron file:

.. sourcecode:: bash

    SHELL=/bin/bash
    */10 * * * * root source /var/www/mysite/virtualenvs/dev/bin/activate && /var/www/mysite/build/dev/manage.py some_custom_command > /dev/null
    
Update - have been informed of a much simpler technique that works for most
cases: simply run manage.py using the python executable of your virtualenv:

.. sourcecode:: bash

    */10 * * * * root /var/www/mysite/virtualenvs/dev/bin/python /var/www/mysite/build/dev/manage.py some_custom_command > /dev/null

I didn't spot this one to start with as our settings configuration required a
environmental variable to be used to indicate which settings file to use. This
variable was set within the activate script, hence why the source command was
needed. It turns out that this can just be set in the cron file too:

.. sourcecode:: bash

    DJANGO_CONF=conf.dev
    */10 * * * * root /var/www/mysite/virtualenvs/dev/bin/python /var/www/mysite/build/dev/manage.py some_custom_command > /dev/null

Much simpler!
