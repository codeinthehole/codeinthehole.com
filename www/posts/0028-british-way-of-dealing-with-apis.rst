=============================================
The British way of dealing with foreign APIs.
=============================================
-----------------------------------
A bad joke told in Python :: python
-----------------------------------

A bad joke told in Python:

.. sourcecode:: python

    def call_foreign_api(str):
        try:
            foreign_api(str)
        except NotUnderstoodError:
            foreign_api(str.upper())