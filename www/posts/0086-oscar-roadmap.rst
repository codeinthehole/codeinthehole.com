=====================
The road to Oscar 1.0
=====================
----------------------------------------
A plan for 2014  :: django-oscar, django
----------------------------------------

.. image:: /static/images/oscar.png
   :align: right
   :class: noborder

Oscar 0.7 was `released this week`_, a comparatively minor house-keeping release
that allowed us to reduce our pull-request and issue backlogs.  We have a plan
for Oscar through 2014 and this article outlines the roadmap.

.. _`released this week`: http://django-oscar.readthedocs.org/en/latest/releases/v0.7.html

v1.0
----

We're aiming to be v1.0 before the end of the year [*]_.  Oscar has been beta for
nearly two years and its APIs are stabilising. We're ready to commit to the
backward compatibility responsibilities associated with coming out of beta.

Plus, this will help `Tangent Snowball`_ (who sponsor Oscar's development) promote
Oscar to blue-chip or "enterprise" clients, who feel nervous enough using
open-source e-commerce software, let alone *beta* open-source software.

There isn't a lot to do before this milestone. Oscar's philosophy
is to keep the core package lean and flexible, hence we don't have a large
shopping list of features we want to add. Rather, there are a few areas
that need careful review to ensure they are flexible enough. Also, there are a
few topics that we want to research thoroughly in case they have design
implications.

These are detailed here:

.. _`Tangent Snowball`: http://www.tangentsnowball.com/

Product dashboard
~~~~~~~~~~~~~~~~~

The current version uses a one-size-fits-all approach which  is now stretched
to breaking point trying to handle a wide range of scenarios. In particular,
it's not easy to administer group and variant products using the current
implementation [*]_.

A new, carefully considered version will be built that provides separate views
and forms for the different work-flows. The new implementation will be simpler
than the current, provide a superior user experience and be easier
to customise and extend.

This piece of work is scheduled to be looked at by Tangent's UX team shortly
and should land in master over the summer.

Multi-tenancy
~~~~~~~~~~~~~

We're aiming to provide better support for multi-tenanted sites where a single
dashboard is used to manage a product catalogue that can be used across several
sites.  Several people on the mailing list have requested this, and Tangent
have a forthcoming project that will require a form of this.

This poses some tricky design questions around how products, categories and
offers are linked to sites.  It's tempting to slap a new many-to-many
relationship onto every core model that links them to sites, but this may not
be the right approach as it will add extra joins to SQL queries.  Some careful
research is required: we don't want to impair performance for the many to
satisfy the requirements of the few. 

We'll be talking to several people at DjangoCon EU 2014 about how Tangent
can partner with other Oscar implementors to first design the appropriate
handling, and later drive forward an implementation.

Faceted browsing everywhere
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Oscar uses Haystack_ for search (with a preference for Solr_) and has some 
`custom helpers`_ to make working with facets easier.  Facets are great for customers
whenever they're browsing a list of products and it's desirable to allow
faceting on all product browsing views.  This would require using the
search back-end to drive all browsing views.

Some `initial work`_ has been done on this already. We intend to review and merge
this into master soon.

.. _Haystack: http://haystacksearch.org/
.. _Solr: https://lucene.apache.org/solr/
.. _`custom helpers`: https://github.com/tangentlabs/django-oscar/blob/master/oscar/apps/search/facets.py
.. _`initial work`: https://groups.google.com/forum/?fromgroups#!topicsearchin/django-oscar/haystack%7Csort:date%7Cspell:true/django-oscar/7cykIQSS7lw

Research topics
~~~~~~~~~~~~~~~

Some things to look into:

- Oscar ships with a set of translation message files but doesn't currently
  provide built-in support for translating model content into multiple languages. 
  There are `various Django libraries`_ that address this issue already. We need
  to research the best approach (or approaches) and document how to use them with
  Oscar.

- Since Oscar is just a set of apps, it works with all existing 
  `Django CMS packages`_. However, more research is required to find the right way to
  integrate content management. With its "promotions" app, Oscar already
  provides some limited forms of merchandising but it might be better to drop
  this app and provide better hooks for CMS packages to manage all content.
  We'll see.

.. _`various Django libraries`: https://www.djangopackages.com/grids/g/model-translation/
.. _`Django CMS packages`: https://www.djangopackages.com/grids/g/model-translation://www.djangopackages.com/grids/g/cms/ 

Thanks
------

As ever, we're hugely grateful to the work of the community: submitting pull
requests, adding translations, reporting bugs. 

If you'd like to get involved, please see our `contributing guidelines`_.

.. [*] We're using `semantic versioning`_
.. [*] This is driven in part by the fact that Tangent haven't had to build a 
       large-scale clothing site yet.

.. _`contributing guidelines`: http://django-oscar.readthedocs.org/en/latest/internals/contributing/index.html
.. _`semantic versioning`: http://semver.org/

