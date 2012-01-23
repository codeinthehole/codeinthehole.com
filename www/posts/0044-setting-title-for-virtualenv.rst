============================================================
Auto-setting terminal titles for python virtual environments
============================================================
----------------------------------------------------
Keeping your tabs organised :: python, commandlinefu
----------------------------------------------------

Problem
-------
You're a python hacker using virtualenv and virtualenvwrapper on a range of
projects.  After a few hours in the office and much context switching, your
terminal emulator is bursting with open tabs with the unhelpful title 'bash'
and it's difficult to remember which tab is for which project.  This is making
you unhappy.

Solution
--------
Use your ``postactivate`` [#]_ script to set the terminal title when you
activate a virtual environment.  Add something similar to the following to your
``postactivate`` script: 

.. sourcecode:: bash

    TITLE="codeinthehole.com"
    echo -ne "\033]0;$TITLE\007"

Then whenever you start working on a project (using ``workon``), your tab title
will be labelled correctly.

.. [#] which will be somewhere like ``~/.virtualenvs/yourproject/bin/postactivate``.

