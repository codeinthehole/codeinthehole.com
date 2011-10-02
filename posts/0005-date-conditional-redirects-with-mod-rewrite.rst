===========================================
Date conditional redirects with mod_rewrite
===========================================
-------------------------------------------------------------
Using ``mod_rewrite`` to redirect based on the date :: apache
-------------------------------------------------------------

The Apache module mod_rewite is capable of some very cool stuff. One neat trick
is to use the time and date variables to control redirects and URL rewriting.
This is useful if you have a URL that you don't want to be exposed to the world
until a certain date has passed - this could be the case with special offers
and competitions which have a one-off static page that isn't to be revealed
until a specified date.

For example, the following directives specify that a temporary 302 redirect
should be issued for all requests to the URL ``/special_offer`` before a certain
date has passed:

.. sourcecode:: apache

    RewriteCond %{TIME} <20081031000000 
    RewriteCond %{REQUEST_URI} /special_offer.*
    RewriteRule (.*) /offers [L,R=302,QSA]

This means that the ``/special_offer`` page can be prepared and deployed beforehand
and apache will handle the transfer once the publish date has passed. There's a
whole load of other nifty things that can be done in a similar vein such as
returning different style sheets depending on the time of day.

Digressing briefly, debugging Apache directives can be quite tricky when you're
playing around trying to get something to work. I find the easiest thing to do
is to redirect to a URL which contains the variable being tested against. For
example:

.. sourcecode:: apache

    RewriteEngine On 
    RewriteCond %{REQUEST_URI} /debug 
    RewriteRule (.*) /debug/?%{TIME}&%{TIME_DAY} [L,R=302]

Then you can see what the values of ``%{TIME}`` and ``%{TIME_DAY}`` are from the URL
you've been redirected to. There are almost certainly better ways of doing this
but this way is quick and it works.
