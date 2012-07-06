======================================================
Vim macros for adding i18n support to Django templates
======================================================
--------------------------------------------------------
Using macros to automate the boring stuff :: vim, django
--------------------------------------------------------

Problem
--------

You want to add i18n support to an existing project.  One part of this is
modifying all templates to use the ``{% trans "..." %}`` block around all
hard-coded strings. 

When you have a lot of templates, this gets pretty tedious.

Solution
--------

Use Vim macros!

Macro 1 - Convert tag text
~~~~~~~~~~~~~~~~~~~~~~~~~~

To convert

.. sourcecode:: html

    <h1>Welcome to my site</h1>

to

.. sourcecode:: html

    <h1>{% trans "Welcome to my site" %}</h1>

use the macro

.. sourcecode:: vimscript

    vitc{% trans "" %}<ESC>4hp

which breaks down as:

* ``vit`` - select content inside the tag;
* ``c{% trans "" %}`` - change tag content to be ``{% trans "" %}`` while saving the
  original tag content to the anonymous register;
* ``<ESC>4hp`` - move the cursor to the first speech mark and paste the original
  tag contents.  Note that ``<ESC>`` is one key-stroke, not five.

To record the macro, locate the cursor over a tag that you want to convert then
start recording by pressing ``q`` twice (to record the macro to the named
register ``q``).  Then type the characters detailed above and press ``q`` again
to stop recording.

To apply the macro, again locate the cursor over a tag, or the text it contains,
and type ``@q``.  This will save you a lot of key-strokes.

Macro 2 - Convert selected text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To convert

.. sourcecode:: html

    <p>See this image: <img src="/images/1.jpg" /> </p>

to

.. sourcecode:: html

    <p>{% trans "See this image:" %} <img src="/images/1.jpg" /> </p>

enter visual mode and select the text to convert (eg "See this image:") then use the macro

.. sourcecode:: vimscript

    c{% trans "" %}<ESC>4hp

which is the same as the one above but without the tag text selection.


To summarise: Vim's macros are great - learn how to use them.
