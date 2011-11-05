=============================================
Phing trick for avoiding deploying debug code
=============================================
-------------------------------------------------------------------------------------
Using the fu with with phing to prevent further embarassments :: commandlinefu, phing
-------------------------------------------------------------------------------------

As the saying goes:

    Fool me once, shame on you; fool me twice, shame on me

Ensuring mistakes aren't repeated is a commonplace activity for any development
team. This can manifest itself in many ways such as writing regression tests,
stepping up your code reviews, adding stories to a testing plan or humiliating
the developer in question through use of an unusual (dunce's) hat.

We had an issue recently where some debugging code got committed and wasn't
picked up during testing. Naturally, this code was picked up once it hit the
production environment, we put rapidly put a patch in place. An embarrassing
moment but the kind of thing that happens from time to time down in the
trenches.

One possible remedy for this would be to add a new sniff to the in-house coding
standard (which is tested using the `PEAR code sniffer`_ on a SVN pre-commit hook)
to look for debugging code and block the commit if any is found. However, a
quicker solution was to modify our deployment scripts to search the codebase
and bail out if any debug code was found. We use phing as our deployment tool -
here's the appropriate section from our build file:

.. _`PEAR code sniffer`: http://pear.php.net/package/PHP_CodeSniffer/redirected

.. sourcecode:: xml

    <echo msg="Checking codebase for use of var_dump()" />
    <exec command="[ `find ${folder.app.export}/classes -name '*.php' | xargs grep -nr '\(^\s*|\s\+\)var_dump(.*\?);' | wc -l` -eq 0 ]" dir="." checkreturn="true" />

The command here is grepping all PHP files within the SVN export for
occurrences of var_dump. If any such matching lines are found then a non-zero
exit will be returned and the build will fail. We haven't had such an issue
since.