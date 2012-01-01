=========================
Writing good Django tests
=========================
----------------------------------------------------------------------------------
Walking through the steps towards clear, readable tests :: python, django, testing
----------------------------------------------------------------------------------

Let's assume this is the first test of the project.  Start by writing a test that
fails, just to demonstrate that it is being run:

.. sourcecode:: python

    from django.test import TestCase

    class SmokeTests(TestCase):
        def test_for_smoke(self):
            assert False

As you would hope, this fails:

.. sourcecode:: bash

    $ ./manage.py test sso --settings=settings_test

Now, exercise the view in question:

.. sourcecode:: python

    from django.test import TestCase
    from django.test.client import Client

    class SSOViewTests(TestCase):
        def test_unauthenticated_user_gets_redirect(self):
            client = Client()
            url = reverse('sso:index')
            response = client.get(url)
            self.assertEquals(302, response.status_code)

We can make this more readable using the `httplib` library:

.. sourcecode:: python

    import httplib

    from django.test import TestCase
    from django.test.client import Client

    class SSOViewTests(TestCase):
        def test_unauthenticated_user_gets_redirect(self):
            client = Client()
            url = reverse('sso:index')
            response = client.get(url)
            self.assertEquals(httplib.FOUND, response.status_code)

Now add a test for an authenticated user:

.. sourcecode:: python

    import httplib

    from django.test import TestCase
    from django.test.client import Client
    from django.contrib.auth.models import User

    class SSOViewTests(TestCase):

        def test_unauthenticated_user_gets_redirect(self):
            client = Client()
            url = reverse('sso:index')
            response = client.get(url)
            self.assertEquals(httplib.FOUND, response.status_code)

        def test_authenticated_user_gets_form(self):
            user = User.objects.create_user(username='terry',
                                            email='',
                                            password='password')
            client = Client()
            client.login(username='terry', password='password')
            url = reverse('sso:index')
            response = client.get(url)
            self.assertEquals(httplib.OK, response.status_code)

Duplication alert!  Let's move the client instantiation into class ``setUp``

.. sourcecode:: python

    import httplib

    from django.test import TestCase
    from django.test.client import Client
    from django.contrib.auth.models import User

    class SSOViewTests(TestCase):

        def setUp(self):
            self.client = Client()

        def test_unauthenticated_user_gets_redirect(self):
            url = reverse('sso:index')
            response = self.client.get(url)
            self.assertEquals(httplib.FOUND, response.status_code)

        def test_authenticated_user_gets_form(self):
            user = User.objects.create_user(username='terry',
                                            email='',
                                            password='password')
            self.client.login(username='terry', password='password')
            url = reverse('sso:index')
            response = self.client.get(url)
            self.assertEquals(httplib.OK, response.status_code)

Similarly, let's use class attributes for the username and password fixtures:

.. sourcecode:: python

    import httplib

    from django.test import TestCase
    from django.test.client import Client
    from django.contrib.auth.models import User

    class SSOViewTests(TestCase):

        USERNAME = 'terry'
        EMAIL = ''
        PASSWORD = 'password'

        def setUp(self):
            self.client = Client()

        def test_unauthenticated_user_gets_redirect(self):
            url = reverse('sso:index')
            response = self.client.get(url)
            self.assertEquals(httplib.FOUND, response.status_code)

        def test_authenticated_user_gets_form(self):
            user = User.objects.create_user(username=self.USERNAME,
                                            email=self.EMAIL,
                                            password=self.PASSWORD)
            self.client.login(username=self.USERNAME, password=self.PASSWORD
            url = reverse('sso:index')
            response = self.client.get(url)
            self.assertEquals(httplib.OK, response.status_code)


