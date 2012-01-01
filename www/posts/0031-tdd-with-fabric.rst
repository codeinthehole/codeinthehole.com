======================================================
Coloured output while doing TDD with Django and Fabric
======================================================
-----------------------------------------------------
Providing simple coloured feedback :: python, testing
-----------------------------------------------------

I'm a big fan of using PHPUnit with console colours turned on (using the
``--colors`` option). Eg:

.. image:: /static/images/screenshots/phpunit.jpg
    :class: screenshot

It helps gets into the natural "red, green, refactor" rhythm.

I'm currently totally immersed in Django, and greatly miss the lack of colour
support within the "test" management command. A simple workaround for this is
to use Fabric with a few modified color commands. Your fabric file should
include the following:

.. sourcecode:: python

    from fabric.colors import _wrap_with

    green_bg = _wrap_with('42')
    red_bg = _wrap_with('41')

    # Set the list of apps to test
    env.test_apps = "app1 app2"

    def test():
        with settings(warn_only=True):
            result = local('./manage.py test %(test_apps)s --settings=settings_test -v 2 --failfast' % env, capture=False)
        if result.failed:
            print red_bg("Some tests failed")
        else:
            print
            print green_bg("All tests passed - have a banana!")

You can choose your own success and failure messages.

Now we have lovely colours while doing TDD in Django:

.. image:: /static/images/screenshots/fab.jpg
    :class: screenshot