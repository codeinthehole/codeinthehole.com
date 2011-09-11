===========================================
Using an in-memory logger with Celery tasks
===========================================

Problem
=======
You want to be able to capture the logging output for a Celery task
and update a model with this information.

Solution
========
Create an in-memory logging handler::

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

This can be used within your celery task to capture the logging output::

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

Discussion
==========
This is a useful pattern to use.


