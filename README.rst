=================
codeinthehole.com
=================

Nothing special here, I just wanted to write my own blog so I could 
optimise it for my own needs.  Basically, I wanted to write articles 
in RST using vim, then have a simple preview and publish mechanism.

How to publish an article
-------------------------

1.  Create an RST article file within the ``articles`` folder. 
2.  Preview locally using::

    ./manage.py rsb_article articles/my-new-article.rst

    Note this renames the file to include the PK, which is helpful when
    article files are renamed.

3.  Repeat the above steps until you are ready to publish. 
4.  Publish article using::

    fab prod publish:articles/0034-my-new-article.rst

How to update the site
----------------------

Simple::

    fab prod deploy


