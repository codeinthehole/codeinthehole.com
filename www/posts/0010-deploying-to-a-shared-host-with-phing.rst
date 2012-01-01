=====================================================
Deploying to a shared hosting environment using Phing
=====================================================
---------------------------------------------------------------
Using Phing's FtpDeployTask to good effect :: deployment, phing
---------------------------------------------------------------

Deploying applications to shared hosting environments can be a pain when no SSH
access is provided. Consequently, it's hard to avoid using FTP to deploy files
from your development environment to a production server. In such trying
circumstances, it's easy to form self-destructive habits like using
drag-and-drop FTP deployment - a very bad thing. Much better is to write an
automated deployment script so that you can build to production in one clean
step, a key tenet of `The Joel Test`_ for writing better code (highly
recommended). Get deployment right at the start and making major changes to
your application becomes trivial rather than a complete nightmare.

.. _The Joel Test: http://www.joelonsoftware.com/articles/fog0000000043.html

`Phing`_ is great for deploying PHP applications. It's well documented, easy to
use and extend, and works well with other libraries such as PHPunit. Although
it's not inthe current docs for version 2.3.x there is a useful FTP task
(``FtpDeployTask.php``) in Phing 2.3.3 that can be used to create a simple build
script for deploying to shared hosting environments using FTP. Syntax and usage
are trivial given a glance through the source code
(``/usr/share/php/phing/tasks/ext/FtpDeployTask.php`` on Ubuntu systems).

.. _Phing: http://phing.info/

Here's a simple build.xml deployment script for a CodeIgniter project that uses
the FtpDeploy task:

.. sourcecode:: xml

    <?xml version="1.0" ?>
    <project name="Shared hosting deployment" default="deploy-application-files" basedir=".">

        <property name="ftp.host" value="ftp.example.com" />
        <property name="ftp.port" value="21" />
        <property name="ftp.username" value="user" />
        <property name="ftp.password" value="password" />
        <property name="ftp.dir" value="/public_html/" />
        <property name="ftp.mode" value="ascii" />

        <!-- FILESETS -->
        <fileset dir="." id="files.images">
            <include name="images/**/*" />
            <include name="favicon.ico" />
        </fileset>
        <fileset dir="." id="files.application">
            <include name="system/application/**/*" />
            <include name="css/*" />
            <include name="js/*" />
        </fileset>
        <fileset dir="." id="files.system">
            <include name="system/**/*" />
            <exclude name="system/application/**/*" />
            <include name="index.php" />
            <include name="robots.txt" />
            <include name=".htaccess" />
        </fileset>

        <!-- DEPLOYMENT TARGETS -->
        <target name="deploy">
            <echo message="Copying fileset '${deploy.fileset.refid}' to ${ftp.host} in ${ftp.mode} mode" />
            <ftpdeploy 
                host="${ftp.host}" 
                port="${ftp.port}" 
                username="${ftp.username}" 
                password="${ftp.password}"
                dir="${ftp.dir}" 
                mode="${ftp.mode}">
                <fileset refid="${deploy.fileset.refid}" />
            </ftpdeploy>
        </target>
        <target name="deploy-images">
            <echo msg="Deploying image files" />
            <phingcall target="deploy">
                <property name="deploy.fileset.refid" value="files.images" />
                <property name="ftp.mode" value="binary" override="true" />
            </phingcall>
        </target>
        <target name="deploy-application-files">
            <echo msg="Deploying application files" />
            <phingcall target="deploy">
                <property name="deploy.fileset.refid" value="files.application" />
            </phingcall>
        </target>
        <target name="deploy-system-files">
            <echo msg="Deploying system files" />
            <phingcall target="deploy">
                <property name="deploy.fileset.refid" value="files.system" />
            </phingcall>
        </target>
        <target name="deploy-all">
            <phingcall target="deploy-images" />
            <phingcall target="deploy-application-files" />
            <phingcall target="deploy-system-files" />
        </target>
    </project>

As we're forced into using clumsy, out-dated FTP (rather than the wonderful
rsync) to copy the files onto the production server, each deployment overwrites
existing files with the selected fileset and this can be quite time-consuming
for large filesets as it often moves across a load of files that haven't
changed. Using FTP, this is tricky to avoid and probably not worth the effort.
Instead, there are four separate deployment targets that only move specific
subsets of the total application fileset over to the production environment
(split according to the standard CodeIgniter directory structure) - most of the
time we only want to move the "files.application" fileset across. These targets
make use of the extremely useful "phingcall" target which allows a
parameterised "deploy" target to be created which takes a fileset id as an
argument.

With the above build.xml in the root of your project, deploying to production
is now as simple as:

.. sourcecode:: bash

    cd /path/to/application/ && phing deploy-all

although most of the time the following suffices:

.. sourcecode:: bash

    cd /path/to/application/ && phing

Note that FtpDeploy.php has a dependency on the PEAR package Net_Ftp which can
be trivially installed in the usual manner:

.. sourcecode:: bash

    sudo pear install Net_FTP

Of course, this script is overly simplistic and only works well with a single
developer. However, it would be easy to extend to team development by
integrating with SVN so that the latest revision (or designated tag/branch) is
checked out into a temporary directory before being copied over to the
production server.
