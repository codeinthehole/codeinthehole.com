==================
PyPI README badges
==================
-------------------------------------
Shiny badges using crate.io :: python
-------------------------------------

Thanks to `@kuramanga`_, it's now possible to add shiny PyPi badges to your Python project
READMEs that indicate the latest released version on PyPI and the total number
of downloads.

.. image:: /static/images/screenshots/oscar-pypi-badges.png
    :target: https://github.com/tangentlabs/django-oscar
    :class: screenshot
    :alt: django-oscar PyPi badges

This screenshot is taken from `django-oscar`_'s README.

Embed these badges in your own repo as Restructured text:

.. sourcecode:: rst

    .. image:: https://pypip.in/v/$REPO/badge.png
        :target: https://crate.io/packages/$REPO/
        :alt: Latest PyPI version

    .. image:: https://pypip.in/d/$REPO/badge.png
        :target: https://crate.io/packages/$REPO/
        :alt: Number of PyPI downloads

or Markdown:

.. sourcecode:: markdown

    [![PyPi version](https://pypip.in/v/$REPO/badge.png)](https://crate.io/packages/$REPO/)
    [![PyPi downloads](https://pypip.in/d/$REPO/badge.png)](https://crate.io/packages/$REPO/)

The `code is available on Github`_, see also Olivier Lacan's shields_ repo.

.. _`django-oscar`: https://github.com/tangentlabs/django-oscar
.. _`@kuramanga`: https://twitter.com/kuramanga
.. _`code is available on Github`: https://github.com/kura/pypipins
.. _`shields`: https://github.com/olivierlacan/shields
