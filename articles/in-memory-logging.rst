===========================================
Using an in-memory logger with Celery tasks
===========================================

----------------------------------------------------------------------------------------------------
Creating a custom logging handler that allows output to be captured so it can be written to a model.
----------------------------------------------------------------------------------------------------

Problem
=======
You want to be able to capture the logging output for a Celery task
and update a model with this information [1]_.

Do something with ``python manage.py something``.

Solution
========
Create an in-memory logging handler

.. sourcecode:: python

    import logging

    class TempHandler(logging.Handler):
        """
        Specialist logger class that records log messgaes to memory
        so they can be read out afterwards.
        """
        def __init__(self):
            self.messages = []
            logging.Handler.__init__(self)
        
        def emit(self, record):
            self.messages.append(self.format(record))
            
        def messages_str(self):
            """
            Return a single string of all messages
            """
            return "\n".join(self.messages)

This can be used within your celery task to capture the logging output

.. sourcecode:: python

    @task
    def process_model(payload):
        # Assign temporary handler
        logger = logging.getLogger()
        handler = TempHandler()
        logger.addHandler(handler)

        # Process the payload model, writing messages to 
        # the logger
        try:
            process_payload(logger, payload)
        except Exception, e:
            logger.exception(e)

        payload.log_messages = handler.messages_str()
        payload.save()

    xxxxxxxxx|xxxxxxxxx|xxxxxxxxx|xxxxxxxxx|xxxxxxxxx|xxxxxxxxx|xxxxxxxxx|xxxxxxxxx|

And here is some PHP.

.. sourcecode:: php

    <?php
    $a = 100;

    class Dave()
    {
        public function __construct($name)
        {
            $this->name = $name;
        }
    }


Discussion
==========
This is a useful pattern to use.

-----------------------

.. [1] This is the text in the footnote
