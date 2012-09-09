===========================================================
Prefer WebTest to Django's test client for functional tests
===========================================================
-------------------------------------------------------
Superior functional tests for Django :: django, testing
-------------------------------------------------------

Since watching Carl Meyer's superb '`Testing and Django`_' talk, I've been using
Ian Bicking's WebTest_ library for functional tests, via django-webtest_.  I've
been really impressed and I'd like to stress one of Carl's points - that using
WebTest for functional tests is superior to using the Django client.

.. _django-webtest: http://pypi.python.org/pypi/django-webtest
.. _WebTest: http://webtest.pythonpaste.org/en/latest/index.html
.. _`Testing and Django`: http://pyvideo.org/video/699/testing-and-django

Why?
====

Several reasons - here's a few:

* WebTest allows you to model a user's experience much more closely as it is
  smart about mark-up.  Instead of hand-crafting GET and POST requests, you can
  use the WebTest API to follow links and submit forms - this is what users
  actually do.  As a result, your tests more accurately capture user stories.

* A corollary to the last point is that writing functional tests with WebTest is
  both easier and quicker than using Django's test client.  It's much simpler to
  fill in forms that contruct complicated arrays of POST data - this is
  particularly noticable with formsets.

* The WebTest response object supports `several ways of parsing the response
  HTML`_, making it easy to make complicated assertions about the response.

.. _`several ways of parsing the response HTML`: http://webtest.pythonpaste.org/en/latest/index.html#parsing-the-body

Watch from 29:48 in Carl's talk for further details.

Example functional test
=======================

Consider this story from a functional spec:

    A staff member can upload a CSV to create new credit allocations for
    customers.

Here's a WebTest for this:

.. sourcecode:: python

    from django_webtest import WebTest
    from django.core.urlresolvers import reverse
    from django.contrib.auth.models import User
    from django_dynamic_fixture import G

    from myproject.credits import api


    class TestAnAdmin(WebTest):

        def setUp(self):
            self.staff = G(User, is_staff=True)
            self.customer = G(User, username='10000', is_staff=False)

        def test_can_upload_a_csv_to_create_allocations(self):
            index = self.app.get(reverse('credits-index'), user=staff)

            # Specify the file content to upload and submit the form
            form = index.forms['upload_form']
            # CSV content should be: username, credits, start_date, end_date
            content = "10000,250,2012-01-01,2013-01-01"
            form['file'] = 'credits.csv', content
            form.submit()

            # Check that an allocation has been created
            self.assertEqual(250, api.balance(customer))
            self.assertEqual(1, api.allocations(customer).count())

As you can see, using WebTest allows the story to captured in a simple and
readable test.  This is based on a real functional test from a current project
of mine.  Writing the above test took about 2 minutes.

Other useful testing libraries
------------------------------

The example test uses django_dynamic_fixture_ to create users, specifying
only the attributes relevant to the test.

.. _django_dynamic_fixture: http://paulocheque.github.com/django-dynamic-fixture/

Note also the mildly unusual naming convention of the example TestCase and
method are because I use django_nose_ with the 'spec' plugin from the pinocchio_
library.  This causes the nose output to read like the stories from your
functional spec:

.. _django_nose: https://github.com/jbalogh/django-nose
.. _pinocchio: http://darcs.idyll.org/~t/projects/pinocchio/doc/

.. sourcecode:: bash

    $ ./manage.py test tests/functional/eshop/credits_tests.py

    nosetests --verbosity 1 tests/functional/eshop/credits_tests.py --with-spec -x -s

    An admin
    - can upload a csv to create allocations

    ----------------------------------------------------------------------
    Ran 1 tests in 0.269s

This is a useful way of running functional tests.  It also pushes you towards
splitting your tests suites into more carefully named, tightly-focussed test cases - rather than
bundling disparate tests into the same test case.

Summary
=======

Use WebTest for your functional tests - you won't regret it.
