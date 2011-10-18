===============================
Deploying cron jobs using Phing
===============================
---------------------------------------------------------------
A phing pattern for deploying cron scripts :: phing, deployment
---------------------------------------------------------------

Deploying applications that depend on cron-jobs can be a pain. However, Phing
can be used to make such deployments easy - here's how...

Consider an application folder structure as follows::

    /builds
        /development
        /test
        /stage
    /src
        /cron.d
            appname-__BUILD__-order-processing
        /scripts
            /order-processing
                handle-ready-to-ship-orders.php
                handle-cancellations.php
                ...
        /public
        /classes
            ...

All development work takes place within the ``/src`` folder while the ``/builds/*``
folders are used as targets in deployment. This system allows multiple builds
to happily co-exist on the same server and the whole application infrastructure
to be moved between servers easily as the structure in source control mirrors
that of the server.

In this example e-commerce app, we have a number of scripts (in ``/src/scripts``)
that handle order-processing which need to be called periodically by the cron
daemon. A naive approach in deployment would be to export the codebase to an
appropriate build folder but then edit the server's crontab by hand and add the
appropriate lines to run these scripts.

This isn't such a great idea though as it relies on that most unreliable
facility, human memory, to ensure the build is fully deployed - this creates an
unnecessary overhead which is bound to lead to mistakes. Furthermore, the
overhead acts as a deterrent for using asynchronous jobs within an application,
limiting the app in terms of what it can do. As far as I am aware, there is no
easy way to automatically update a user's crontab automatically.

A much better way is to create a number of scripts which specify the cron tasks
and are deployed to the /etc/cron.d folder. In the above example, these are
stored in /src/cron.d and would look something like:

.. sourcecode:: bash

    15 * * * *   root   /var/www/ecommerce.com/builds/__BUILD__/scripts/handle-ready-to-ship-orders.php > /dev/null 2>> /var/log/cron.errors.log
    35 * * * *   root   /var/www/ecommerce.com/builds/__BUILD__/scripts/handle-cancellations.php > /dev/null 2>> /var/log/cron.errors.log

(Note that, for some reason, a blank line is required at the end of this file
in order for the script to be run by cron.) Here, the ``__BUILD__`` is a tokenised
parameter which will be replaced during deployment to configure the path to the
appropriate script - a phing trick I've described previously.

One further complication is that if both the dev, test and stage builds are
running on the same server, then the scripts deployed to ``/etc/cron.d`` could
clobber each other as they have the same name within each build. This can be
neatly side-stepped using the Phing's glob mapper to replace the ``__BUILD__``
component of the file to be the appropriate build name (similar to how the
paths are configured within the file itself).

This is probably best illustrated with a sample phing script which takes the
build name (eg "development") as a parameter:

.. sourcecode:: xml

    <xml version="1.0" encoding="UTF-8"?>
    <project>
        <target name="deploy">
            ...
            <delete>
                <fileset dir="/etc/cron.d/">
                    <include name="appname-${build.name}-*" />
                </fileset>
            </delete>
            <copy todir="/etc/cron.d/"> 
                <filterchain>
                    <replacetokens begintoken="__" endtoken="__">
                        <token key="BUILD" value="${build.name}" />
                    </replacetokens>
                </filterchain>
                <mapper type="glob" from="appname-__BUILD__-*" to="appname-${build.name}-*" />
                <fileset dir="${path.to.build}/cron.d">
                    <include name="appname-__BUILD__-*" />
                </fileset>
            </copy>
        </target>
    </project>

The illustrated snippet does two things:

Deletes any previous scripts for this build from ``/etc/cron.d`` (this is why we
namespace the files with "appname" to prevent accidentally removing a system
file).
Copies the new scripts into ``/etc/cron.d`` while replacing the token ``__BUILD__``
with the build name in both the file contents and file names.
After separate deployments for dev and stage, we should find the following::

    /etc
        /cron.d
            appname-development-order-processing
            appname-stage-order-processing
            ...

where, for instance, the contents of
``/etc/cron.d/appname-development-order-processing`` would be:

.. sourcecode:: bash

    * * * * *   root   /var/www/ecommerce.com/builds/development/scripts/handle-ready-to-ship-orders.php
    * * * * *   root   /var/www/ecommerce.com/builds/development/scripts/handle-cancellations.php
    ...

Having automatic and reliable deployment of cron-jobs in place is quite
liberating. Suddenly, lots of application processing can be done asynchronously
without worrying about the overhead of maintaining the appropriate crontabs by
hand.
