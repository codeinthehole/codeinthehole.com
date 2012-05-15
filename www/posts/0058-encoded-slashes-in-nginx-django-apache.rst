=======================================
Django, Nginx, WSGI and encoded slashes
=======================================
-----------------------------------------------------------------------------------
Encoded slashes have a hard time getting through to Django :: django, apache, nginx
-----------------------------------------------------------------------------------

Problem
=======

You are serving a Django application using Nginx to proxy to an Apache server
running mod_wsgi and you want to allow slashes in your URL keywords.  

For example, you may want to edit some attribute of the page at URL ``/``; hence,
you want to use a URL regex of the form:

.. sourcecode:: python

    url(r'/edit/page/(?P<page_url>.*)/$', ...)

and use the URL ``/edit/page/%2F/`` to edit this page, where the third path
segment is URL-encoded.

This works fine in local development using Django's ``runserver`` but not when
Nginx/Apache are involved.  Both services will 'process' the incoming request in
a way that collapses repeating slashes.  Django sees the above request path as
``/edit/path``.

Solution
--------

First, in order to get django to encode slashes, you need to pass an empty
string to the ``urlencode`` template filter.

.. sourcecode:: python

    {% url edit-page url|urlencode:"" %}

Next ensure Nginx's ``proxy_pass`` configuration is transmitting the URL in
'unprocessed form' by omitting the path on the proxied server argmenent.  That is, use:

.. sourcecode:: nginx

    proxy_pass http://localhost:80;

instead of:

.. sourcecode:: nginx

    proxy_pass http://localhost:80/;

The only different between these two examples is the trailing slash.  See the
`nginx documentation for proxy_pass`_ for more details on what
'unprocessed' means.

.. _`nginx documentation for proxy_pass`: http://wiki.nginx.org/HttpProxyModule

Next, alter your Apache config to include the ``AllowEncodedSlashes``
directive to ensure Apache recognises encoded slashes:

.. sourcecode:: apache

    <VirtualHost \*>
        ...
        AllowEncodedSlashes On
        ...
    </VirtualHost>

Finally modify your WSGI script to ensure Django gets the slashes
in its ``PATH_INFO`` environmental variable which it uses for resolving the URL
to a view function:

.. sourcecode:: python

    # ... other WSGI stuff: setting up path, virtualenv etc

    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    import django.core.handlers.wsgi
    _application = django.core.handlers.wsgi.WSGIHandler()

    import urllib
    def application(environ, start_response):
        environ['PATH_INFO'] = urllib.unquote(environ['REQUEST_URI'].split('?')[0])
        return _application(environ, start_response)

The key change is using the ``REQUEST_URI`` variable to set ``PATH_INFO``.  We
pluck the path component from ``REQUEST_URI`` and use ``urllib.unquote`` to
ensure encoded slashes are decoded.


Discussion
----------

The ``PATH_INFO`` variable is decoded by mod_wsgi, effectively collapsing repeated slashes.  
The ``REQUEST_URI`` is the raw request and so it's possible to use it to ensure
encoded slashes make it through to Django.

Further reading
---------------

* This `StackOverflow answer`_ describes a similar technique to solve this problem for Google App Engine.
* A `Google Groups discussion`_ of the issue.

.. _`StackOverflow answer`: http://stackoverflow.com/questions/3040659/how-can-i-receive-percent-encoded-slashes-with-django-on-app-engine
.. _`Google Groups discussion`: https://groups.google.com/forum/?fromgroups#!topic/django-users/31oV1WhuAZ4
