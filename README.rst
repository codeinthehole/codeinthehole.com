=================
codeinthehole.com
=================

Nothing special here - I just wanted to write my own blog so I could 
optimise it for my own needs.  The aim was to write articles 
in RST using vim, then have a simple preview and publish mechanism.

The blog is a simple Django project which uses RST files as a source
for creating a simple Article model. Fabric is used to publish articles 
to the production site.

See `Rewriting codeinthehole.com`_ for more details.

.. _`Rewriting codeinthehole.com`: http://codeinthehole.com/writing/rewriting-codeintheholecom/

Usage
=====

How to publish an article
-------------------------

Create an RST article file within the ``articles`` folder::

    vim posts/my-new-article.rst

Preview locally using::

    ./manage.py rsb_article posts/my-new-article.rst
    ./manage.py runserver

Note this renames the file to include the PK, which is helpful when article
files are renamed, but annoying if you still have it open in vim. You have been
warned.

Repeat the above steps until you are ready to publish, then run::

    fab prod publish:posts/0034-my-new-article.rst

Push it to Github so you've got a backup.

How to update the site
----------------------

If you have changes to the django project or the static assets, you'll need to
run::

    fab prod deploy

to deploy.
