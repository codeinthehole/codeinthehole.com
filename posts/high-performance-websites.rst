===========================================
High Performance Web Sites by Steve Souders
===========================================
-------------------------------
A short review :: apache, books
-------------------------------

.. image:: /static/images/bookcovers/9780596529307.jpg
   :align: right

High Performance Web Sites (HPWS) is essentially a book-length exposition of
the `YSlow extension to Firebug`_ augmented with case studies of popular US
websites. YSlow itself links to some `explanation paragraphs`_ regarding the
various guidelines that are used to grade the performance of a website.
However, even for those familiar with this documentation, HPWS is still an
excellent resource on how the performance of a web app can be tuned.

.. _Yslow extension to Firebug: http://developer.yahoo.com/yslow/
.. _explanation paragraphs: http://developer.yahoo.com/performance/rules.html

Chapter by chapter, HPWS introduces a new guideline and expounds the underlying
rationale, giving illustrations of the HTTP requests with and without the
suggested improvement. For instance, the use of far-future Expires HTTP headers
is an easy-win recommendation that prevents unnecessary requests once a
browser's cache has been primed. This is something I've used on several sites
previously, employing the following Apache directives to add Expires headers to
the HTTP:

.. sourcecode:: apache

    <IfModule mod_expires.c>
        ExpiresActive on
        ExpiresByType image/jpg “access plus 2 years”
        ExpiresByType image/jpeg “access plus 2 years”
        ExpiresByType image/gif “access plus 2 years”
        ExpiresByType text/css “access plus 2 days”
        ExpiresByType image/js “access plus 2 days”
        ExpiresDefault ”access plus 1 days”
    </IfModule>

Additional areas where I found out something new include:

* The performance hit that using @import directives within CSS files has.
* How the "Cache control" and "Etags" HTTP headers are often interpreted together
  by browsers to determine whether to make a request.
* How the choice of domains to use for serving content must be balanced against
  the extra DNS look-up costs that each new domain incurs.

Many of the performance guidelines can be adhered to easily, by making a few
adjustments to the Apache configuration of your site; However, some
performance-enhancing measures come at a cost to the development process (such
as keeping all javascript in one large, minified file). Such costs can be
mitigated by having a careful one-step build process that handles the
conversion of easy-to-use development files to more performance-savvy
production files. Nevertheless, in many cases, one has to decide where the
balance between performance and inconvenience in development lies.

It's quite a short book at 137 pages, but definitely a worthwhile addition to
any company library.
