=================================
Embedding HTML in Django messages
=================================
--------------------------------------------------------------------
Using ``extra_tags`` to flag up HTML-safe messages :: django, python
--------------------------------------------------------------------

Problem
-------

You want to embed HTML within a message using `Django's messages framework`_.  

This is a reasonably common requirement - for instance, it's
common to want to include a link within the message, perhaps pointing the user
towards a sign-in or registration page.

.. _`Django's messages framework`: https://docs.djangoproject.com/en/dev/ref/contrib/messages/

This problem exists as of Django 1.4 but may be solved within the framework in
later versions.

Solution
--------

Use the ``extra_tags`` `keyword argument`_ to pass a flag indicating that the message is
safe for rendering without escaping.  For example:

.. _`keyword argument`: https://code.djangoproject.com/browser/django/branches/releases/1.4.X/django/contrib/messages/api.py#L15

.. sourcecode:: python

    from django.contrib import messages

    def some_view(request):
        ...
        messages.success(request, 
                         'Here is a <a href="/">link</a>.',
                         extra_tags='safe')
        ...

Then use some simple template logic to determine whether to use the ``safe``
filter:

.. sourcecode:: html+django

    <ul>
        {% for message in messages %}
        <li class="{{ message.tags }}">
            {% if 'safe' in message.tags %}
                {{ message|safe }}
            {% else %}
                {{ message }}
            {% endif %}
        </li>
        {% endfor %}
    </ul>

Discussion
----------

It's tempting to use the ``safe`` filter for all messages but this opens up a
XSS security hole if you are not careful as it's easy to include user input
verbatim in the message.  For instance:

.. sourcecode:: python

    from django.contrib import messages

    def some_view(request):
        code = request.GET['code']
        ...
        messages.success(request, "'%s' is not valid voucher code" % code)

leads to an XSS hole if the ``safe`` filter is used on all messages as the
contents of ``request.GET['code']`` cannot be trusted.  It's better to
explicitly indicate which messages can be safely rendered without escaping.

Taken from a `Stack Overflow answer`_.

.. _`Stack Overflow answer`: http://stackoverflow.com/questions/2053258/how-do-i-output-html-in-a-message-in-the-new-django-messages-framework