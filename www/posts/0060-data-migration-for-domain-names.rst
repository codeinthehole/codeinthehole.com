=========================================
A data migration for every Django project
=========================================
-------------------------------------------------------------
No more embarassing emails from example.com :: django, python
-------------------------------------------------------------

How to use a South data migration to avoid accidentally sending emails from example.com.

Problem
=======

Consider the following snippet from Django's docs [#]_ for sending a confirmation email:

.. sourcecode:: python

    from django.contrib.sites.models import Site
    from django.core.mail import send_mail

    def register_for_newsletter(request):
        current_site = Site.objects.get_current()
        send_mail(
            'Thanks for subscribing to %s alerts' % current_site.name,
            'Thanks for your subscription. We appreciate it.\n\n-The %s team.' % current_site.name,
            'editor@%s' % current_site.domain,
            [user.email]
        )

Here the domain for the email sender is taken from the 'current site' instance,
which is controlled by `Django's 'Sites' framework`_ and accessible by a custom
method on the manager of the  ``Site`` model.

By default, a ``Site`` instance is created with domain and display name
'example.com' and you have to correct these values.  This is often done by hand
using the admin suite.

However, as with any manual change, it's easy to forget and you'll often find
Django projects sending email from ``editor@example.com``.  Highly embarassing.

.. _`Django's 'Sites' framework`: https://docs.djangoproject.com/en/dev/ref/contrib/sites/?from=olddocs

Solution
========

Automation, of course!  We can use a South data migration to set the domain and
display name correctly in each environment.  

First, ensure that each environment has settings for the domain
and site name.  

.. sourcecode:: bash

    # conf/test.py
    ...
    DOMAIN_NAME = 'test.project.client.tangentlabs.co.uk'
    SITE_NAME = 'project - client (test)'

    # conf/stage.py
    ...
    DOMAIN_NAME = 'stage.project.client.tangentlabs.co.uk'
    SITE_NAME = 'project - client (stage)'

This snippet assumes you are using a set-up similar to that outlined by `David
Cramer`_, where an environmental variable specifies an additional settings file
to import.  You don't have to use this method; employing a ``settings_local.py``
file for each environment works just as well. 

.. _`David Cramer`: http://justcramer.com/2011/01/13/settings-in-django/

Next, create a data migration to set the domain and display name correctly in each
environment.  This migration sits most naturally in the ``django.contrib.sites``
app, but since that's in Django's core, it's not an option.  
You could use an existing app within your project to house the migration or
perhaps create a simple 'core' or 'data' app to house data migrations that alter
3rd party apps.  

Since we're not using the actual app where the ``Site`` model
is defined, we must employ South's ``--freeze`` option to ensure the ``Site`` model
is available to the migration.

.. sourcecode:: bash

    python manage.py datamigration <appname> create_domains --freeze=sites

Finally implement the ``forwards`` method:

.. sourcecode:: python

    from south.v2 import DataMigration
    from django.conf import settings

    class Migration(DataMigration):

        def forwards(self, orm):
            Site = orm['sites.Site']
            site = Site.objects.get(id=settings.SITE_ID)
            site.domain = settings.DOMAIN_NAME
            site.name = settings.SITE_NAME
            site.save()

Then your next deployment to each environment will perform the update.

.. [#] See https://docs.djangoproject.com/en/1.4/ref/contrib/sites/#getting-the-current-domain-for-display
