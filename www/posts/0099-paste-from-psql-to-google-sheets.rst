==========================================
Copying Postgres output into a spreadsheet
==========================================
----------------------------------------------------
Quick tip on tweaking the output of psql :: postgres
----------------------------------------------------

I often need to grab information from a Postgres database and paste it into a
spreadsheet for sharing with others. Google Sheets needs the pasted
data to be tab-separated in order to be correctly split into columns. This isn't
the default behaviour for psql but here's how to configure psql's output to get
it.

At a psql prompt, switch to unaligned output

.. sourcecode:: psql

    => \a

and set the field separator to a tab character:

.. sourcecode:: psql

    => \f '\t'

then the output from subsequent ``SELECT ...`` statements can be cleanly pasted
into your Google Doc.

    

    
