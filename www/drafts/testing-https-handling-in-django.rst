================================
Testing HTTPS handling in Django
================================

Problem
=======
You want to test how your application handles HTTPS

Solution
========
Use the following to simulate a HTTPS request using the Django test client:

..sourcecode:: python

    client = Client()
    client.get(url, **{'wsgi.scheme': 'https'})

Discussion
==========

