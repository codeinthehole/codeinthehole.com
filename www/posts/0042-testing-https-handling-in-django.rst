================================
Testing HTTPS handling in Django
================================
------------------------------------------------------------------------
Spoofing a HTTPS request using the Django test client :: django, testing
------------------------------------------------------------------------

Problem
=======

You want to test how your application handles HTTPS requests.

Solution
========

Use the following to simulate a HTTPS request using the Django test client:

.. sourcecode:: python

    from django.test.client import Client

    client = Client()
    response = client.get(url, **{'wsgi.url_scheme': 'https'})

Discussion
==========

The standard way to test for a HTTPS request is using the ``is_secure`` method
of the ``django.http.HttpRequest`` class [#]_ and its subclasses.  As of Django 1.3, the
implementation of this method checks whether an environmental variable ``HTTPS``
is equal to "on":

.. sourcecode:: python

    # django/http/__init__.py

    class HttpRequest(object):
        ... 
        def is_secure(self):
            return os.environ.get('HTTPS') == 'on'

However, Django's test client uses the ``django.core.handlers.wsgi.WSGIRequest`` class
for requests.  This class provides an alternative implementation:

.. sourcecode:: python

    # django/core/handlers/wsgi.py
    
    class WSGIRequest(http.HttpRequest):
        ...
        def is_secure(self):
            return 'wsgi.url_scheme' in self.environ \
                and self.environ['wsgi.url_scheme'] == 'https'

Hence why need to pass the ``wsgi.url_scheme`` keyword arg when making the
request.

Note that the unpacked dictionary syntax is required as it's the only way of
specifying a keyword arg that includes a dot.

.. [#] See https://docs.djangoproject.com/en/dev/ref/request-response/
