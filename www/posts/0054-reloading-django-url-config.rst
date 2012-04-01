=================================
How to reload Django's URL config 
=================================
---------------------------------------------------------------------------------
A rare sighting of the ``reload`` function in the wild :: django, testing, python
---------------------------------------------------------------------------------

Problem
-------

For some reason, you need to reload your Django URL config.

Normally, the root URL config will be imported and stored in memory when your
server process starts up.  Occasionally though, you may want to reload it.  This
can be the case if your URL configuration changes depending on certain
parameters.  

Solution
--------

You can reload the URL config using the following snippet:

.. sourcecode:: python

    import sys
    from django.conf import settings

    def reload_urlconf(urlconf=None):
        if urlconf is None:
            urlconf = settings.ROOT_URLCONF
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])

Discussion
----------

This was a problem I needed to solve while testing the checkout process for
`django-oscar`_.  Oscar uses a setting flag to optionally add decorators to
certain URLs, and hence I needed to patch the setting and reload the URLs as
part of the set-up for a test.

.. _`django-oscar`: https://github.com/tangentlabs/django-oscar

This was achieved in the following way, where the setting
``OSCAR_ALLOW_ANON_CHECKOUT`` is set to ``True`` and the URL config is reloaded.

.. sourcecode:: python

    import sys
    from django.conf import settings

    ...

    class EnabledAnonymousCheckoutViewsTests(ClientTestCase, CheckoutMixin):

        def reload_urlconf(self):
            if settings.ROOT_URLCONF in sys.modules:
                reload(sys.modules[settings.ROOT_URLCONF])
            return import_module(settings.ROOT_URLCONF)

        def test_shipping_address_requires_session_email_address(self):
            with patch_settings(OSCAR_ALLOW_ANON_CHECKOUT=True):
                self.reload_urlconf()
                response = self.client.get(reverse('checkout:shipping-address'))
                self.assertIsRedirect(response)

There's probably a better way of doing this, but it wasn't apparent to me when
working on this problem today.
