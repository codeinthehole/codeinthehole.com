========================
Bootstrapped virtualenvs
========================
--------------------------------------------------------------
Using ``postmkvirtualenv`` to prime ``postactivate`` :: python
--------------------------------------------------------------

The excellent virtualenvwrapper_ supports a ``postmkvirtualenv`` script to
bootstrap your virtual environments. Here's a useful implementation:

.. _virtualenvwrapper: https://bitbucket.org/dhellmann/virtualenvwrapper..

.. sourcecode:: bash

    #!/usr/bin/env bash

    # Grab project name from virtualenv name
    NAME=$(basename $VIRTUAL_ENV)

    # Set terminal title on postactivate
    echo "title $PROJECT" > $VIRTUAL_ENV/bin/postactivate

    # Change directory to root of project on postactivate. We assume the
    # mkvirtualenv is being run from the root of the project. This line 
    # will need to edited later if not.
    echo "cd $PWD" >> $VIRTUAL_ENV/bin/postactivate

    # Run postactivate now to get the title set
    source $POSTACTIVATE

This ensures that a new virtualenv has a ``postactivate`` script which:

1.  Sets the terminal title to that of the virtualenv
2.  Changes directory to the root of the project

By convention, such a script lives in ``~/.virtualenvs/postmkvirtualenv``.

Note that the ``title`` function is defined in my ``~/.bashrc`` as:

.. sourcecode:: bash

    function title() {
        echo -ne "\033]0;$1\007"
    }

As someone who develops in iTerm and Terminal, automatically setting the tab
titles is a useful navigation aid.

.. image:: /static/images/screenshots/terminal-titles.png

There are more `tips and tricks`_ available in the virtualenvwrapper docs.

.. _`tips and tricks`: http://virtualenvwrapper.readthedocs.org/en/latest/tips.html
