==========================
Multi-DB testing in Django
==========================

I've had some fun getting a test suite to run for a multi-DB Django project.
This post is just to detail the resolutions to the problems I've encountered.

In this instance, we're using three databases:

* ``default`` - The write master for the customer facing site
* ``read_slave`` - The read slave for the customer site
* ``process`` - Processing server

In production, these are all MySQL databases running on dedicated servers.
