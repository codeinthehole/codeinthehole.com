==========================================
A deferred logging file handler for Django
==========================================
---------------------------------------------------------------
Using a setting to control where file logs go :: django, python
---------------------------------------------------------------

At Tangent we handle environment-specific configuration of Django projects using
`the method outlined by David Cramer`_.  This involves distinguishing between core settings 
(which we keep in ``core/default.py``) and environment specific settings
(eg ``core/stage.py``, ``core/test.py``).  The standard ``settings.py`` module
imports all defaults and then uses a enviromental shell variable to determine
which environment settings module to import.

.. _`the method outlined by David Cramer`: http://justcramer.com/2011/01/13/settings-in-django/

A problem
---------

One tricky issue with this arrangement is logging to file.  Ideally, we want to define a
single ``LOGGING`` dict in the default settings but have file logging use an
environment-specific folder.  For example, logging to file in the test environment goes to
``/var/log/project/test/`` while stage goes to a file in
``/var/log/project/stage``.

One solution
------------

This can be solved by using a string template for the ``filename``
argument to each ``FileHandler`` in the ``LOGGING`` setting:

.. sourcecode:: python

    # conf/default.py

    LOGGING = {
        'version': 1,
        ...
        'handlers': {
            'error_file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': '{log_root}errors.log',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['error_file'],
                'level': 'ERROR',
                'propagate': False,
            },
        }
    }

then importing the default ``LOGGING`` dict into your
environment-specific settings and formatting each filename with the correct
path:

.. sourcecode:: python

    # conf/test.py

    from conf.default import LOGGING

    LOG_ROOT = '/var/log/project/test/'
    for handler in LOGGING['handlers'].values():
        if handler['class'] == 'logging.FileHandler':
            handler['filename'] = handler['filename'].format(log_root=LOG_ROOT)

This works but is rather clunky.  For instance, the default ``LOGGING`` setting (without an
environmental override) will lead to an error .

Another solution
----------------

Another, possibly more elegant, solution is to use a specialisd logging handler
that defers evaluation of the filepath until it tries to log a record.

.. sourcecode:: python

    from logging import FileHandler as BaseFileHandler
    import os


    class DeferredFileHandler(BaseFileHandler):

        def __init__(self, filename, *args, **kwargs):
            self.filename = filename
            kwargs['delay'] = True
            BaseFileHandler.__init__(self, "/dev/null", *args, **kwargs)

        def _open(self):
            # We import settings here to avoid a circular reference as this module
            # will be imported when settings.py is executed.
            from django.conf import settings
            self.baseFilename = os.path.join(settings.LOG_ROOT, self.filename)
            return BaseFileHandler._open(self)

Now, all we need to do is use the new handler in our ``LOGGING`` dict:

.. sourcecode:: python

    # conf/default.py

    LOGGING = {
        'version': 1,
        ...
        'handlers': {
            'error_file': {
                'level': 'INFO',
                'class': 'deferred_filelogger.DeferredFilehandler',
                'filename': 'errors.log',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['error_file'],
                'level': 'ERROR',
                'propagate': False,
            },
        }
    }

and specify a ``LOG_ROOT`` setting for each environment:

.. sourcecode:: python

    # conf/test.py

    LOG_ROOT = '/var/log/project/test/'

Such a logger is part of django-oscar_, but I've packaged it up separately so it
can be used in non-Oscar projects.  The package is called
django-deferred-filelogger_ and can be installed from PyPI using:

.. sourcecode:: bash

    $ pip install django-deferred-filelogger

.. _django-oscar: https://github.com/tangentlabs/django-oscar/blob/master/oscar/core/logging/handlers.py
.. _django-deferred-filelogger: https://github.com/codeinthehole/django-deferred-filelogger 

