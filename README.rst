=================
codeinthehole.com
=================

Nothing special here, I just wanted to write my own blog so I could 
optimise it for my own needs.  Basically, I wanted to write articles 
in RST using vim, then have a simple preview and publish mechanism.

The blog is a simple Django project which uses RST files as a source
for creating a simple Article model.

How to publish an article
-------------------------

1.  Create an RST article file within the ``articles`` folder::

    vim posts/my-new-article.rst

2.  Preview locally using::

    ./manage.py rsb_article posts/my-new-article.rst
    ./manage.py runserver

    Note this renames the file to include the PK, which is helpful when
    article files are renamed, but annoying if you still have it open in vim.

3.  Repeat the above steps until you are ready to publish. 

4.  Publish article using::

    fab prod publish:posts/0034-my-new-article.rst

How to update the site
----------------------

Simple::

    fab prod deploy


