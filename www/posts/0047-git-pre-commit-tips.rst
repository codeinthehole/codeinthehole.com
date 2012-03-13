====================================
Tips for using a git pre-commit hook
====================================
-----------------------------------
Yet another git tips article :: git
-----------------------------------

Here's a few tips for using a `Git pre-commit hook`_.

.. _`Git pre-commit hook`: http://book.git-scm.com/5_git_hooks.html


Keep your hook script in source control
---------------------------------------

Commit your hook script (say ``pre-commit.sh``) at the root of your project and 
include the installation instructions in your README/documentation to encourage all
developers use it.

Installation is nothing more than:

.. sourcecode:: bash

    ln -s ../../pre-commit.sh .git/hooks/pre-commit

Then everyone benefits from running the same set of tests before committing and
updates are picked up automatically.

Stash unstaged changes before running tests
-------------------------------------------

Ensure that code that isn't part of the prospective commit isn't tested
within your pre-commit script.  This is missed by many sample pre-commit scripts
but is easily acheived with ``git stash``:

.. sourcecode:: bash

    # pre-commit.sh
    git stash -q --keep-index

    # Test prospective commit
    ...

    git stash pop -q

The ``-q`` flags specify quiet mode.


Run your test suite before each commit
--------------------------------------

Obviously.  

It's best to have a script (say ``run_tests.sh``) that encapsulates the 
standard arguments to your test runner so your pre-commit script doesn't fall out
of date.  Something like:

.. sourcecode:: bash

    # pre-commit.sh
    git stash -q --keep-index
    ./run_tests.sh
    RESULT=$?
    git stash pop -q
    [ $RESULT -ne 0 ] && exit 1
    exit 0

where a sample ``run_tests.sh`` implementation for a Django project may look
like:

.. sourcecode:: python

    # run_tests.sh
    ./manage.py test --settings=settings_test -v 2

Skip the pre-commit hook sometimes
----------------------------------

Be aware of the ``--no-verify`` option to ``git commit``.  This bypasses the 
pre-commit hook when committing, which is useful is you have just manually 
run your test suite and don't need to see it run again when committing.

I use a git aliases to make this easy:

.. sourcecode:: bash

    # ~/.bash_aliases
    alias gc='git commit'
    alias gcv='git commit --no-verify'

Search your sourcecode for debugging code
-----------------------------------------

At some point, someone will try and commit a file containing

.. sourcecode:: bash 

    import pdb; pdb.set_trace()

or some other debugging code.  This can be easily avoided using the ``pre-commit.sh`` file 
to grep the staged codebase and abort the commit if forbiden strings are found.

Here's an example that looks for ``console.log``:

.. sourcecode:: bash

    FILES_PATTERN='\.(js|coffee)(\..+)?$'
    FORBIDDEN='console.log'
    git diff --cached --name-only | \
        grep -E $FILES_PATTERN | \
        GREP_COLOR='4;5;37;41' xargs grep --color --with-filename -n $FORBIDDEN && echo 'COMMIT REJECTED Found "$FORBIDDEN" references. Please remove them before commiting' && exit 1

It's straightforward to extend this code block to search for other terms.
