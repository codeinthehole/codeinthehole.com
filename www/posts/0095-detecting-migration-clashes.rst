===================================
Avoiding clashing Django migrations
===================================
------------------------------------------------------------
A simple Travis test to avoid frustration :: django, testing
------------------------------------------------------------

Managing South migrations on a multi-developer Django project can be painful.
Developers working on separate branches will often create migrations for the
same app with the same migration number [1]_. When merged into master,
these clashing migrations can cause deployment hiccups as South will complain if
migrations are applied out of order.  

There are various techniques available for dealing with this [2]_, but what we do
at Yoyo_ is test for such clashes as part of our Travis continuous integration.

This is done by calling a ``makefile`` target from ``.travis.yml``:

.. sourcecode:: yaml

    # .travis.yml

    language: python

    python:
        - 2.7

    install:
        - make virtualenv

    script
        - make test
        - make migration_test

where the ``migration_test`` target is:

.. sourcecode:: make

    # makefile

    MIGRATION_CLASHES=$(shell find . -type f -name "*.py" | grep -o ".*/migrations/[0-9]\+" | sort | uniq -c | awk '$$1 > 1 {print $$0}')
    migration_test:
        [ -n $(MIGRATION_CLASHES) ] && exit 1 || true

Here the ``$(shell ...)`` call extracts the app name and migration number from
all migration files then uses ``awk`` to look for clashes.  If any are found,
the Travis build will fail and the console output should reveal which apps have
clashes. 

This works best if you only allow fast-forward commits into master (something we
do at Yoyo_). Doing this forces you to merge master back into your pull request
branch and allows Travis to catch migration clashes before it is merged. Then
any conflicts can be resolved by renumbering or recreating any migrations not
yet merged to master.


.. [1] I'm only talking about Django versions less than 1.7 - I'm not sure if
       this is still an issue in more modern Django versions.

.. [2] As noted by the `South docs`_, you can run the migrations with the
       ``--merge`` option although this generally means a manual intervention in your
       deployment process which isn't ideal.

.. _Yoyo: http://justyoyo.com/
.. _`South docs`: http://south.readthedocs.org/en/latest/tutorial/part5.html
