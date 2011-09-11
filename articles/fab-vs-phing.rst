================
Fabric vs. Phing
================

As far as I'm aware, fabric and phing are the most popular deployment tools for Python and PHP
projects respectively.  I've used them both extensively; this article details some of the 
main differences.



----------
Subtitle 1
----------

Subtitle 2
----------


Phing is programming XML
------------------------
Genuinely not nice.

Fabric works better when you have a multi-server infrastructure
---------------------------------------------------------------
You can use roles to have certain targets only apply to certain servers::

    from fabric import roles

    @roles('webserver')
    def collect_static():
        pass

Fabric is just a wrapper around Bash.

