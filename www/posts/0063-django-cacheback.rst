====================================================
Cacheback - asynchronous cache refreshing for Django
====================================================
----------------------------------------------------------------------------------------
A simple caching library that uses Celery to refresh stage cache items :: django, python
----------------------------------------------------------------------------------------

Inspired by `Jacob Kaplan-Moss`_'s excellent talk "`Django doesn't scale`_" at
this year's OSCon, I've put together a Django package for re-populating caches
asynchronously.  

.. _`Jacob Kaplan-Moss`: http://jacobian.org/

It provides a simple API for wrapping expensive read operations that caches
results and uses Celery_ to repopulate items when they become stale.  It can be
used as a decorator for simple cases but provides an extensible class for more
fine-grained control.  It also provides helper classes for working with querysets.

.. _Celery: http://celeryproject.org/
.. _`Django doesn't scale`: http://www.oscon.com/oscon2012/public/schedule/detail/24030

The package is MIT-licensed, published to PyPI_ and the source is available on
Github_.  It's best explained with an ...

.. _PyPI: http://pypi.python.org/pypi/django-cacheback
.. _Github: https://github.com/codeinthehole/django-cacheback

Example
=======

Consider a view that renders a user's tweets:

.. sourcecode:: python

    from django.shortcuts import render
    from myproject.twitter import fetch_tweets

    def show_tweets(request, username):
        return render(request, 'tweets.html', 
                      {'tweets': fetch_tweets(username)})

This works fine but the ``fetch_tweets`` function involves a HTTP round-trip and
is slow.  Enter caching.

Basic caching
-------------

Performance can be improved using Django's `low-level cache API`_:

.. _`low-level cache API`: https://docs.djangoproject.com/en/dev/topics/cache/?from=olddocs#the-low-level-cache-api
        
.. sourcecode:: python

    from django.shortcuts import render
    from django.cache import cache
    from myproject.twitter import fetch_tweets

    def show_tweets(request, username):
        return render(request, 'tweets.html', 
                      {'tweets': fetch_cached_tweets(username)})

    def fetch_cached_tweets(username):
        tweets = cache.get(username)
        if tweets is None:
            tweets = fetch_tweets(username)
            cache.set(username, tweets, 60*15)
        return tweets

Now tweets are cached for 15 minutes after they are first fetched, using the
twitter username as a key.  This is obviously a performance improvement but the
shortcomings of this approach are:

* For a cache miss, the tweets are fetched synchronously, blocking code execution
  and leading to a slow response time.

* This in turn exposes exposes the view to a '`cache stampede`_' where
  multiple expensive reads run simultaneously when the cached item expires.
  Under heavy load, this can bring your site down.

.. _`cache stampede`: http://en.wikipedia.org/wiki/Cache_stampede

Procrastinate instead
---------------------

For most applications, it's not actually essential that the cache is refreshed
immediately - it's acceptable to return stale results and update the cache
asynchronously (so-called `'Eventual Consistency'`_).  This is desirable as it
means all reads are fast and prevents cache stampedes.  

.. _`'Eventual Consistency'`: http://en.wikipedia.org/wiki/Eventual_consistency

Using Celery
------------

Consider an alternative implementation that uses a Celery task to repopulate the
cache.

.. sourcecode:: python

    import datetime
    from django.shortcuts import render
    from django.cache import cache
    from myproject.tasks import update_tweets

    def show_tweets(request, username):
        return render(request, 'tweets.html', 
                      {'tweets': fetch_cached_tweets(username)})

    def fetch_cached_tweets(username, lifetime=60*15):
        item = cache.get(username)
        if item is None:
            # Scenario 1: Cache miss - return empty result set and trigger a refresh
            update_tweets.delay(username, lifetime)
            tweets = None
        else:
            tweets, expiry = item
            if expiry > datetime.datetime.now():
                # Scenario 2: Cached item is stale - return it but trigger a refresh
                update_tweets.delay(username, lifetime)
        return tweets

where the ``myproject.tasks.update_tweets`` task is implemented as:

.. sourcecode:: python

    import datetime
    from celery import task
    from django.cache import cache
    from myproject.twitter import fetch_tweets

    @task()
    def update_tweets(username, ttl):
        tweets = fetch_tweets(username)
        now = datetime.datetime.now()
        cache.set(username, (tweets, now+ttl), 2592000) 

Some things to note:

* Items are stored in the cache as tuples ``(data, expiry_timestamp)`` using
  Memcache's maximum expiry setting (2592000 seconds).  By using this value, we
  are effectively bypassing memcache's replacement policy in favour of our own.

* As the comments indicate, there are two replacements scenarios to consider:

  1.  Cache miss.  In this case, we don't have any data (stale or otherwise) to
      return.  In the example above, we trigger an asynchronous refresh and
      return an empty result set.  In other scenarios, it may make sense to
      perform a synchronous refresh.

  2.  Cache hit but with stale data.  Here we return the stale data but trigger
      a Celery task to refresh the cached item.

This pattern of re-populating the cache asynchronously works well.  Indeed it is
the basic of the Cacheback package.

Using Cacheback
---------------

Here's the same functionality implemented using the ``cacheback`` function:

.. sourcecode:: python

    from django.shortcuts import render
    from django.cache import cache
    from myproject.twitter import fetch_tweets
    from cacheback.decorators import cacheback

    def show_tweets(request, username):
        return render(request, 'tweets.html', 
                      {'tweets': cacheback(60*15, fetch_on_miss=False)(fetch_tweets(username))})

The ``cacheback`` function will generate a cache key based on the module path of
the wrapped function and the passed args and kwargs.  It then checks the cache
and if there isn't a valid result it will serialise the function and its args so
it can be executed asynchronously by a Celery task.

The ``cacheback`` function can also be used as a decorator:

.. sourcecode:: python

    from cacheback import cacheback

    @cacheback(15*60)
    def fetch_tweets(username):
        ...

Or for more fine-grained control: using a subclass of ``cacheback.base.Job``:

.. sourcecode:: python

    from django.shortcuts import render
    from django.cache import cache
    from myproject.twitter import fetch_tweets
    from cacheback.base import Job

    def show_tweets(request, username):
        return render(request, 'tweets.html', 
                      {'tweets': FetchTweets().get(username)})

    class FetchTweets(Job):
        expiry = 60 * 15

        def fetch(self, username):
            return fetch_tweets(username)

While only the ``fetch`` method must be implemented, the ``cacheback.Job`` class
provides several other overridable methods that provide fine-grained control of
the caching process. 

Interested?
===========

Check-out the `documentation`_ for more information.  Comments and feedback
welcome.

.. _`documentation`: http://django-cacheback.readthedocs.org/en/latest/
        