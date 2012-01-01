===================================
Console logging to STDOUT in Django
===================================
------------------------------------------------------
Undocumented option required to avoid STDERR :: django
------------------------------------------------------

Problem
=======

By default in Django, the documented console handler emits to STDERR, but you
want it to use STDOUT instead.

Solution
========

Use the following LOGGING config in your settings to specify a different output stream:

.. sourcecode:: python

    import sys
    LOGGING = {
        'handlers': {
            'console':{
                'level':'INFO',
                'class':'logging.StreamHandler',
                'strm': sys.stdout
            },
            ...
        }
    }
    
Discussion
==========

`Django's logging docs`_ detail the following logging configuration for a console handler:

.. _`Django's logging docs`: https://docs.djangoproject.com/en/dev/topics/logging/#an-example

.. sourcecode:: python

    LOGGING = {
        ...
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        ...
    }

however, the default output stream for ``logging.StreamHandler`` is STDERR. The
extra keyword argument in the solution alter this behaviour to use STDOUT.

Logging to STDERR means that any output from cron jobs is emailed to root. A
more desirable behaviour is for only errors to trigger emails, while normal
output can be logged to file.
