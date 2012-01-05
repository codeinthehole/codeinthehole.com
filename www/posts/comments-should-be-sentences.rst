============================
Comments should be sentences
============================
--------------------------------------------
Good etiquette for writing comments :: style
--------------------------------------------

If you commentting style takes this form:

.. sourcecode:: python

    #unhide synced rows
    model.filter(...).update(is_hidden=True)

you're making me angry.

I've never understood why people don't have a space after the ``#``.  It just makes things
so #pointlessly #hard #to #read.

If you're just annotating what is going on then this belongs in a logger so the
timings can be tracked.

.. sourcecode:: python

    self.logger.info("Unhiding synced rows")
    ...

Example good comment:

.. sourcecode:: python

    # Unsync all rows that are currently hidden so that the 
    # script can determine which to re-apply to offers to after
    # depoyment.
    ...




