====================
E-commerce practices
====================

People assume you're using Java



Other people suck!

Celery is awesome
-----------------

Split tasks up as much as possible and throw more workers at the problem:

- deployment
- CSV processing

PK trick for processing large tables


Audit needs to be central
-------------------------

Models should have as many datetime fields as possible

    class NielsenBatch(models.ModelBase):
        ...
        date_created = models.DateTimeField(auto_now_add=True)
        date_downloaded = models.DateTimeField(null=True)
        date_processed = models.DateTimeField(null=True)

Prefer NULLable dates to boolean


OO design
---------

Facades are good: shipping / payment / comms

Django
------

Transaction middleware


Logging

Use the debug/info settings predently

Use lots of models
------------------

Models in Django are cheap and easy - when it comes to processing, use them with gay abandon.

Create models that represent transactions with 3rd parties

Use date_fields instead of booleans
