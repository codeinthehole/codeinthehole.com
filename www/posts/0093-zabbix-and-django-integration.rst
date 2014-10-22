==================================================
Integrating Django application metrics into Zabbix
==================================================
----------------------------------------------------------------------------
A simple how-to for feeding Django metrics into Zabbix :: django, monitoring
----------------------------------------------------------------------------

At Tangent_, we use Zabbix_ for monitoring and alerting. This is a note-to-self on
how to configure application monitoring.  

.. _Tangent: http://www.tangentsnowball.com
.. _Zabbix: http://www.zabbix.com/

Management command
~~~~~~~~~~~~~~~~~~

You need a script that prints out a value to STDOUT. A simple management command
suffices:

.. sourcecode:: python

    from django.core.management.base import BaseCommand, CommandError

    class Command(BaseCommand):

        def handle(self, *args, **options):
            if not args:
                print self.usage()
                return
            method_name = 'fetch_%s' % args[0]
            if not hasattr(self, method_name):
                raise CommandError("No method found with name '%s'" % method_name)
            print getattr(self, method_name)(args[1:])

        def usage(self):
            fetchers = [m for m in dir(self) if m.startswith('fetch')]
            descriptions = []
            for fetcher in fetchers:
                method = getattr(self, fetcher)
                docstring = method.__doc__.strip() if method.__doc__ else "<no description>"
                descriptions.append(" - %s : %s" % (
                    fetcher.split("_")[1], docstring))
            return "Available fetchers:\n%s" % "\n".join(descriptions)

This uses dynamic dispatch to call "fetcher" methods with name "fetch_%s" where
the first argument defines the format variable. Eg, a method:

.. sourcecode:: python

    def fetch_num_users(self):
        """
        Fetch number of users
        """
        return User.objects.all().count()

is called via:

.. sourcecode:: bash

   $ ./manage.py application_metric num_users

It's trivial to add more ``fetch_*`` methods to emit additional metrics.

Zabbix plugin
~~~~~~~~~~~~~

Hook this up to Zabbix by first creating a plugin script which calls the
management command, passing on an arg:

.. sourcecode:: bash

    $ cat /etc/zabbix/plugins/application
    #!/bin/bash

    source /path/to/virtualenv/bin/activate && /path/to/project/manage.py application_metric $1

then create the Zabbix "UserParameter" declaration which calls the plugin script:

.. sourcecode:: bash

    $ cat /etc/zabbix/zabbix_agentd.conf.d/application.conf
    UserParameter=application[*],/etc/zabbix/plugins/application $1

The ``application[*]`` syntax means that you can configure various "Items" in
Zabbix like ``application[num_orders]`` and ``application[num_users]`` and the bracketed
string will get passed all the way through to the management command.

Now restart Zabbix to pick up the new conf file:

.. sourcecode:: bash

    $ /etc/init.d/zabbix-agent restart

Zabbix dashboard
~~~~~~~~~~~~~~~~

In the Zabbix web dashboard add new "Items" that use this new "UserParameter".  Add a new
"Item" by navigating through ``Configuration > Hosts > Items > Create item``.
In the resulting form, set the "Key" to, say, ``application[num_users]`` to pass
``num_users`` as the first argument through to the management command.

And that's it: this metric will now be collected by Zabbix and can be used for graphing
and alerting.
