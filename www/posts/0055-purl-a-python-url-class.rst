=======================================
purl - immutable URL objects for Python
=======================================
------------------------------------------------------------------------------
An immutable URL class designed for easy inspection and manipulation :: python
------------------------------------------------------------------------------

Working with URLs in Python feels clunky when it should be pleasant.  In
urlparse_ and urllib_, the standard library has all the functionality you need,
but the code you have to write is often cumbersome and unclear. 

.. _urlparse: http://docs.python.org/library/urlparse.html
.. _urllib: http://docs.python.org/library/urllib.html

For instance, here's a typical test method that makes an assertion about a query
parameter:

.. sourcecode:: python

    import urlparse

    def test_url_has_correct_query_parameter(self):
        url = get_url_from_somewhere()
        parse_result = urlparse.parseurl(url)
        query_params = urlparse.parse_qs(parse_result.query)
        self.assertEqual('testing', query_params['q'][0])

Not terrible, but could be more concise. I would prefer something like:

.. sourcecode:: python

    from somelibrary import URL

    def test_url_has_correct_query_parameter(self):
        url = URL.from_string(get_url_from_somewhere())
        self.assertEqual('testing', url.query_param('q'))

Further, when working with webservices, you often need to build URLs
programmatically but it just isn't easy enough in python.  You often end up
using string formatting:

.. sourcecode:: python

    import urllib

    URL_TEMPLATE = 'https://github.com/%s?w=%s' 
    def get_github_url(username):
        return URL_TEMPLATE % (urllib.quote(username), '0')

A preferable API might look something like:

.. sourcecode:: python

    from somelibrary import URL

    BASE_URL = URL.from_string('https://github.com/') 
    def get_github_url(username):
        return BASE_URL.path_segment(0, username).query_param('w', 0)

This is a toy example, the problem is much worse when building more complicated
URLs.

purl 
----

.. warning::

    Warning - the code examples below are from version 0.2 of purl - please
    consult the `Github documentation`_ for the latest reference.

.. _`Github documentation`: https://github.com/codeinthehole/purl

So I wrote a utility class to scratch this itch.  It's a simple immutable
``URL`` class that uses jQuery-style overloading of the attribute methods to be
both accessors and mutators.

Install with:

.. sourcecode:: python

    pip install purl


Construct URL instances as follows:

.. sourcecode:: python

    from purl import URL

    # Explicit constructor
    u = URL(scheme='https', host='www.google.com', path='/search', query='q=testing')

    # Use factory class-method
    u = URL.from_string('https://www.google.com/search?q=testing')

    # Chain mutator methods (which each return a new instance)
    u = URL().scheme('https').host('www.google.com').path('search').query_param('q', 'testing')

    # Combine to suit your use-case
    u = URL.from_string('https://www.google.com').path('search') \
                                                 .query_param('q', 'testing')

There's a full range of inspection methods:

.. sourcecode:: python

    # Simple attributes
    u.scheme()      # 'https'
    u.host()        # 'www.google.com' 
    u.domain()      # 'www.google.com' - alias of host
    u.port()        # None (only returns something if explicitly set)
    u.path()        # '/search'
    u.query()       # 'q=testing'
    u.fragment()    # ''

    # Convenience methods for inspecing path, query and host
    u.path_segment(0)                   # 'search'
    u.path_segments()                   # ('search',)
    u.query_param('q')                  # 'testing'
    u.query_param('q', as_list=True)    # ['testing']
    u.query_param('lang', default='GB') # 'GB'
    u.query_params()                    # {'q': 'testing'}
    u.has_query_param('q')              # True
    u.subdomains()                       # ['www', 'google', 'com']
    u.subdomain(0)                       # 'www'

Each accessor method is overloaded to be a mutator method too, similar
to the jQuery API.  Since the URL class is immutable, any mutation will return a
new URL instance.

.. sourcecode:: python

    u = URL.from_string('https://github.com/codeinthehole')

    # Access
    u.path_segment(0) # returns 'codeinthehole'

    # Mutate (creates a new instance)
    new_url = u.path_segment(0, 'tangentlabs') # returns new URL object

Here's a fancier example of building a URL:

.. sourcecode:: python

    u = URL().scheme('https')\
             .host('github.com')`\
             .path_segment(0, 'codeinthehole')\
             .path_segment(1, 'purl')\
    print u.as_string()

    # returns 'https://github.com/codeinthehole/purl'

`Source and further details on Github`_.

.. _`Source and further details on Github`: https://github.com/codeinthehole/purl

Alternatives
------------

There are a couple of URL classes already for python - however neither had the
exact API I was looking for.  

* mxURL_ - Part of the 'eGenix.com mx Base Distribution', this has quite a
  comprehensie API.  It comes bundles with other utility modules with the
  'egenix-mx-base' package.

.. _mxURL: http://www.egenix.com/products/python/mxBase/mxURL/

* URLObject_ - There's nothing wrong with this implementation - it's very
  similar to my one above.  The API's not quite to my tastes but that's purely
  subjective thing. 

.. _URLObject: https://github.com/zacharyvoase/urlobject/

Discussion
----------

There is a `discussion of this post`_ on `/r/Python`_.

.. _`discussion of this post`: http://www.reddit.com/r/Python/comments/sjkab/purl_an_immutable_url_class/
.. _`/r/python`: http://www.reddit.com/r/Python/

