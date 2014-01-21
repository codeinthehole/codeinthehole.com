=====================================================
Command-line tips for effective release announcements
=====================================================
------------------------------------------------------------------------------
Git tips for writing release notes :: git, commandlinefu, django, django-oscar
------------------------------------------------------------------------------

We finally `released Oscar 0.6`_ last week.  The process brought home the
importance of writing your release notes as you go rather than at the end.
It's a real pain to extract the key changes from 1200 commits spread over the
last 8 months.  Lesson learnt.  

This article is largely a note-to-self in case I have to repeat the process.
However, if you do find yourself in a similar position, here are a few
command-line tricks for analysing your git history.

.. _`released Oscar 0.6`: http://django-oscar.readthedocs.org/en/latest/releases/v0.6.html

Analysing codebase changes since a tag
--------------------------------------

Basics: browse commits since the last tagged release

.. sourcecode:: bash

    $ git log 0.5..0.6

The ``--name-status`` option for ``git diff`` is useful for analysing codebase changes
between two commits.  For instance, you can view changes to a particular directory:

.. sourcecode:: bash

   $ git diff --name-status 0.5..0.6 oscar/apps/address

which can be useful if thousands of files have changed and you want to review
each package individually.

Extensions include finding deleted files:

.. sourcecode:: bash

   $ git diff --name-status 0.5..0.6 | grep "^D"

or all new migration files:

.. sourcecode:: bash

    $ git diff --name-status 0.5..0.6 | grep "^A.*migrations/[0-9]"

which is important for projects like Oscar which ship with database migrations.

Determine changes template block names
--------------------------------------

Since Oscar allows customisation of templates and overriding template blocks,
we try and document any changes to template block names.  The process here is
more involved and requires two temporary files generated with this command:

.. sourcecode:: bash

   $ grep -or "{% block .* %}" oscar/templates/oscar | \
       awk 'BEGIN {FS=":"} {split($2, parts, " "); print $1, parts[3]}'

This writes out each pairs of filename and template block name:

.. sourcecode:: csv

   oscar/templates/oscar/403.html title
   oscar/templates/oscar/403.html error_heading
   oscar/templates/oscar/403.html error_message
   oscar/templates/oscar/404.html title
   oscar/templates/oscar/404.html error_heading
   oscar/templates/oscar/404.html error_message
   ...

To compare the template blocks from each release, we create two temporary files
and analyse the diff:

.. sourcecode:: bash

   $ git checkout 0.5
   $ grep -or "{% block .* %}" oscar/templates/oscar | \
       awk 'BEGIN {FS=":"} {split($2, parts, " "); print $1, parts[3]}' >
       /tmp/templates-0.5.txt
   $ git checkout 0.6
   $ grep -or "{% block .* %}" oscar/templates/oscar | \
       awk 'BEGIN {FS=":"} {split($2, parts, " "); print $1, parts[3]}' >
       /tmp/templates-0.6.txt
   $ vimdiff /tmp/templates-0.{5,6}.txt

I imagine there's a better way to do this but I couldn't find one.

.. note::

   This is a Django specific technique, but the general approach is quite
   useful for analysing changes between two codebases.

Updating an ``AUTHORS`` files
-----------------------------

Oscar's ``AUTHORS`` file contains all contributors with 15 or more commits in
the master branch.  We generate this file automatically.

You can sort authors by number of commits:

.. sourcecode:: bash

    $ git shortlog -sn master | head
      2992  David Winterbottom
       355  Maik Hoepfel
       167  Sebastian Vetter
       166  Jon Price
       120  Andrew Ingram
        73  Asia Biega
        65  Oliver Randell
        49  Eleni Lixourioti
      ...

and extend this to find authors with more than a certain number of commits

.. sourcecode:: bash

    $ THRESHOLD=15
    $ git shortlog -sn master | awk '$1 >= $THRESHOLD {$1="";print $0}' | cut -d" " -f2-

Note, ``git shortlog`` uses a ``.mailmap`` file to aggregate commmits from the same
committer where their name or email were different in the commit history.

Using this command, we can create a new ``AUTHORS`` file containing all
contributors with greater than 15 commits on the master branch:

.. sourcecode:: bash

    $ git shortlog -ns master | awk '$1 >= $THRESHOLD {$1="";print $0}' | \
        cut -d" " -f2- > AUTHORS

Notifying contributors
----------------------

If you have a patch accepted into a project,  it's useful to know when a
formal release has been cut that includes said patch.  Before then, you might be
linking your project to a fork and maintaining a work-around within your
codebase.

As the project maintainer, you might assume that such people are already
subscribed to your project mailing list, or following your project Twitter
stream. However, there's a more thorough way to notify contributors that their
patch is in a release: you can email them.

To do this, extract the email addresses of committers whose patches are in the new release:

.. sourcecode:: bash

    $ git log 0.5..0.6 --format='%aE' | sort | uniq

and CC these addresses in your mailing list release announcement.

Even better, you can only grab the addresses of *new* contributors to the
project, where the release is the first to contain one of their commits.  We do
this by extracting two lists of email addresses and employing the lovely but
neglected ``comm`` command to pluck the email addresses that only exist in the
latest release:

.. sourcecode:: bash

    $ comm -13 <(git log 0.5 --format='%aE' | sort | uniq) \
        <(git log 0.5..0.6 --format='%aE' | sort | uniq)

Note the first input is all contributors up to release 0.5, while the second
is contibutors to the 0.6 release only.

``comm`` is an extremely useful command for selecting lines common between two
files, or exclusive to one.  The ``-13`` options indicate to exclude lines
exclusive to the first file (``-1``) and lines common to both (``-3``).

Summarising changes
-------------------

If your release isn't large, your release notes could include a summary of the
contained commits; this is useful for minor point releases.  You can use ``git shortlog`` to do this:

.. sourcecode:: bash

    $ git shortlog 0.5..0.6 --no-merges
    David Winterbottom (661):
          Add defaults to the counts on the product summary dashboard page
          Tidy up urls.py and settings.py
          Use mirrors when pip installing the demo site
          Install django-oscar-stores
          Add link to stores page in footer
    ...

You can even use ``--format`` to provide links to Github commits:

.. sourcecode:: bash

    $ git shortlog 0.3.4..0.4 --no-merges --format="%s (https://github.com/tangentlabs/django-oscar-stores/commit/%h)" 

This won't always be appropriate if your release if there are thousands of
commits.
