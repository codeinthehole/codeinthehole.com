===========================
Rewriting codeinthehole.com
===========================
------------------------------
Yet another RST blog :: django
------------------------------

I rewrote this blog recently with the following aims:

* to make it as easy as possible to create a new article, using `reStructuredText`_ (RST)
  as the base for each article; 

.. _`reStructuredText`: http://docutils.sourceforge.net/rst.html

* to clean up and simplify the design, focussing on the readability of
  articles that include code snippets.

I knew that there were various static blogs out there, with many supporting
RST, but I still fancied the challenge of crafting something specific to my
needs.  There's nothing wrong with wheel re-invention if you want to learn
about wheels.

This article is a short summary.

Technology
----------

Django, Fabric and pygments - the `source is on github`_.  I intend to pull
out the generic blogging code into a separate library, reStructuredBlog, at 
some point, hence the "rsb" acronym used in the codebase.

.. _`source is on github`: http://github.com/codeinthehole/codeinthehole.com

Writing an post
---------------

My ideal for writing a blog post is:

1. Use vim to create a ``.rst`` file for the article;
2. Preview the article locally;
3. Publish to the remote server

This translates to the following:

Write
~~~~~

.. sourcecode:: bash

    vim posts/my-new-article.rst 

Preview
~~~~~~~

.. sourcecode:: bash

    ./manage.py rsb_article posts/my-new-article.rst
    ./manage.py runserver

This converts the RST file into a instance of ``rsb.models.Article``, plucking 
out the title, subtitle and any tags in the process.

Rinse and repeat the write and preview steps until happy.

Publish
~~~~~~~

.. sourcecode:: bash

    fab prod publish posts/0036-my-new-article.rst

This copies the RST file up to the remote server and re-runs
the ``rsb_article`` management command to create the article in the
production database.

Design
------

.. image:: /static/images/bookcovers/9781119998952.jpg
   :align: right

I recently read the excellent "Design for Hackers" by David Kadavy.  
Duly inspired, I attempted to rework the design to be clean and pleasing 
on the eye.  The color scheme is deliberately kept simple; the fonts used
are Verdana, `Droid Serif`_ and `Inconsolata`_.

.. _`Droid Serif`: http://www.google.com/webfonts/specimen/Droid+Serif
.. _`Inconsolata`: http://www.google.com/webfonts/specimen/Inconsolata

I was also influenced by the clean look of the personal sites
of `Steve Losh`_, `Zach Holman`_ and `Armin Ronacher`_.

.. _`Steve Losh`: http://stevelosh.com/
.. _`Zach Holman`: http://zachholman.com/
.. _`Armin Ronacher`: http://lucumr.pocoo.org/

Overall
-------

I'm pleased that:

* The site isn't painfully ugly like the old;
* I can write articles easily and using my favourite tools (vim + RST);
* I can write articles on the tube on the way home;
* Github is now my backup of both code and content.  For instance, 
  you can `view the source of this article`_.

.. _`view the source of this article`: http://github.com/codeinthehole/codeinthehole.com/www/posts/0038-restructured-blog.rst

Since I switched to Disqus for comments, I decided to drop all the old ones
(not that were that many), since I wasn't sure it was possible to migrate
Apologies to the comment authors.
