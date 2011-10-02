====================================
Following log files with ``tail -f``
====================================

-----------------------------------------------------------
Simple trick to watch progressive updates to a file :: Bash
-----------------------------------------------------------

UNIX is a majestic onion of discovery. Every day a new layer of understanding 
can be peeled away to give some new pungent goodness. Today's was the 'follow' 
option of the tail command.

It's commonplace to use tail for viewing the recent entries to a log file:

.. sourcecode:: bash

    tail /var/log/apache2/error.log

Much more useful is set the 'follow' option so that, rather than echoing to 
STDOUT and returning control to the prompt - tail continues to watch the file in 
question and echos additional lines to the terminal. This can be very useful 
during development - I often leave a terminal open watching the error logs while 
I develop - so that I can quickly pounce on any errors that pop up.

.. sourcecode:: bash 

    tail -f my-app-error.log

Return control to the command prompt using CTRL+C (or run as a background 
process using &). This can be quite useful for monitoring the error logs of 
production sites where echoing error messages and warnings to the screen would 
be unacceptable.
