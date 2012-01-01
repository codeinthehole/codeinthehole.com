===============================
Logging and management commands
===============================

Here's a common pattern:

..sourcecode:: python

    import logging    

    class LoggingCommand(BaseCommand):
        
        def handle(self, *args, **options):
            self.logger = logging.getLogger(__name__)
            try:
                self.run(*args, **options)
            except Exception, e:
                self.logger.exception(e)
                raise

        def run(*args, **options):
            raise NotImplementedException("A run method needs to be impemented")

This ensures that any exceptions are correctly logged within your log file so exceptions
can be traced back to what was going on.

It's also a good practice to modify your ``manage.py`` to handle uncaught exceptions:

..sourcecode:: python

    asdf

    
