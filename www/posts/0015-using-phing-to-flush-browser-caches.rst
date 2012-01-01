============================================
Using a Phing filter to flush browser caches
============================================
-------------------------------------------------------------------
Using a filterchain to set a cache-busting query parameter :: phing
-------------------------------------------------------------------

A quick `Phing`_ tip that's made my life easier when deploying new versions of
`commandlinefu.com`_. 

.. _`Phing`: http://phing.info/trac/
.. _`commandlinefu.com`: http://www.commandlinefu.com/

One of the `key performance recommendations`_ from Steve Souders' excellent "High
Performance Websites" is to use Expires HTTP headers to set far-future
expiration dates for your site components (such as images, Javascript files and
CSS stylesheets).  This way, browsers can cache the files between requests
giving a performance boost to your site.  Assuming you're using Apache for
serving, the following settings can be used to set these headers for all
Javascript and CSS files (there are a few alternative ways of achieving the
same result):

.. _`key performance recommendations`: http://stevesouders.com/hpws/rule-expires.php

.. sourcecode:: xml

    <FilesMatch "\.(ico|pdf|flv|jpg|jpeg|png|gif|js|css|swf)$">
        Header set Expires "Thu, 15 Apr 2010 20:00:00 GMT"
    </FilesMatch>

The main issue to be aware of using this technique is that, when your
components change, you need to ensure your visitors are forced to download the
latest version rather than using the one cached by their browser.  The only way
to ensure this happens is to use a different URL for the assets in question.
One option might be to rename the files themselves but a more convenient
alternative is to include a query string as part of the request URL (eg ``<script
src="/js/behaviour.js?2009-03-15" type="text/javascript" />``).  Then changing
the query string component is sufficient to force browsers to make a full
request for the new component. 

This works well but is an easy-to-forget overhead for deployment.  However,
this substitution can be automated by making use of the Filters that Phing
provides.  Doing so is trivial: simply insert a tokenised string as the query
string after your asset URLs.  That is:

``<link rel="stylesheet" href="/css/styles.css?~~CACHEBUSTER~~" type="text/css" />``
where the ``~~`` delimiter indicates the token. Then include something like the
following snippet in your Phing deployment script.

.. sourcecode:: xml

    <tstamp>
        <format property="build.datetimestring" pattern="%Y-%m-%d-%H-%M" />
    </tstamp>
    ...
    <target name="create-temp-build" description="Creates a temporary copy of the source files">    
        <echo msg="Copying deployment files into temporary directory" />
        <copy todir="${dev.folder.temp}">
            <filterchain>
                <replacetokens begintoken="~~" endtoken="~~">
                    <token key="CACHEBUSTER" value="${build.datetimestring}" />
                </replacetokens>
            </filterchain>
            <fileset refid="deployment-files" />
        </copy>
    </target>

The filterchain component of the copy task parses the given fileset for
matching tokens that match and replaces them with the given value. In this
example, I'm using timestamps as the replacements as these will ensure a
different query string on each deployment. Doing so ensures that the deployed
HTML includes the lines:

.. sourcecode:: html

    <link rel="stylesheet" href="/css/styles.css?2008-03-15-21-51" type="text/css" />
    <script type="text/javascript" src="/js/site-behaviour.js?2008-03-15-21-51">

which then ensure that all subsequent visitors download the latest versions of
the CSS and javascript files. The above target is taken from a deployment
script I use which creates a temporary snapshot of the codebase that I want to
deploy, but the basic principle of using the replacetokens filter is easily
transferable to any deployment script.
