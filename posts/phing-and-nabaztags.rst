=========================
Phing, Xinc and Nabaztags
=========================
------------------------------------------
Using Phing to command a Nabaztag :: phing
------------------------------------------

Finally got around to setting up continuous integration for some of the
projects that comprise the day-job. We're using the PEAR package Xinc, which
has proved to be excellent thus far - especially as it integrates so well with
my deployment tool of choice: Phing. Part of the fun in setting it up was
looking for suitable feedback mechanisms or devices. Email notifications are a
given but there are a range of more interesting feedback mechanisms available
such as toolbar notifications, remote-controlled lava lamps, or plain
humiliation tactics (such as making the person who broke the build wear the
dunce's hat till it is fixed). By a strange twist of fate there happened to be
an unused Nabaztag in the office: a strange Rabbit-like fellow able to play
sounds, move its ears and activate a selection of brightly colours LEDs
contained in its body. Nabaztags are controlled through a simple HTTP
web-service, with the various actions been specified by GET requests using a
simple API.

Out of the box, Xinc only provides email notifications for feedback but its
design is such that plugins are easy to create. Indeed, Raphael Stolt has
written recently on creating a publisher that uses the Growl notifications
native to Macs. A natural extension to this would be to create an Linux
version, given the inclusion of libnotify in the latest Ubuntu release. That's
not for today though.

The true flexibility in Xinc comes from the phingpublisher publisher, which
allows an arbitrary target to be called from a phing script. Rather than create
a Xinc plugin for the Nabaztag, writing a Phing task seemed to offer more
flexibility as it could then be used in deployment scripts elsewhere.

I've previously created a couple of simple phing tasks for updating a Twitter
status, and interacting with the Unfuddle API. Creating a Nabaztag task was
just a simple extension of these cURL-based tasks. The various attributes
mirror those from the API docs.

======
Name	            Type	    Description	                        Default	        Required
serialNum	        String	    Serial number	                    n/a	            Yes
token	            Integer	    Token number	                    n/a	            Yes
leftEarPosition	    String	    Position of the left ear (0-16)	    n/a	            No
rightEarPosition	String	    Position of the right ear (0-16)	n/a	            No
message	            String	    Message.	                        n/a	            No
messageId	Integer	Message id.	n/a	No
voice	Integer	Voice to use (use the API to fetch the full list)	n/a	No
choreography	String	A string which prescribes the choreography to use (see API docs)	n/a	No
choreographyTitle	Boolean	Choreography title	n/a	No
urlList	Boolean	List of URLs to pass to the Nabaztag (can be used for playing audio files)	n/a	No
checkReturn	Boolean	Whether to check the return code of the request, throws a BuildException if the update fails	false	No

The code for this task can be found in my github repo - to install locally,
export the file to a local phing tasks folder (I use
``/usr/share/php/phing/tasks/my`` on my Ubuntu machine). Having done that, a simple
example build.xml file to exercise the task would be:

.. sourcecode:: xml

    <?xml version="1.0" ?>
    <project name="Example Nabaztag update" basedir=".">
        <taskdef name="nabaztag" classname="phing.tasks.my.NabaztagTask" />
        <target name="build-failure">
            <nabaztag serialNum="${nabaztag.serialNum}" token="${nabaztag.token}" message="The build failed!" voice="US-Liberty" />
        </target>
    </project>

To use this with Xinc, you simply need to called the appropriate target from
your project configuration file. Another toy example:

.. sourcecode:: xml

    <?xml version="1.0"?>
    <xinc>
        <project name="Toy example">
            <configuration>
                    <setting name="loglevel" value="1"/>
                    <setting name="timezone" value="Europe/London"/>
            </configuration>
            <property name="dir" value="/var/xinc/projects/sample"/>
            <cron timer="*/15 * * * *"/>
            <modificationset>
                <svn directory="${dir}" update="true" />
            </modificationset>              
            <builders>
                    <phingBuilder buildfile="${dir}/build.xml" target="build-project"/>
            </builders>
            <publishers>
                <onfailure>
                    <phingpublisher buildfile="${dir}/build.xml" target="build-failure" />
                </onfailure>
            </publishers>
        </project>
    </xinc>

Some of the options for controlling the Nabaztag are only available with the V2
version. The one on my desk is V1 and so I haven't tested every action, I've
just followed the instructions in the API docs. Unfortunately, the Nabaztag
webservice isn't as RESTful as would be desired - it returns a 200 response
code for every request, whether it fails or not. This makes it a touch tricky
to handle failed updates.

Nabaztags are also useful for general reminders - I have the following line in my crontab:

.. sourcecode:: bash

    15 18 * * 5 curl "http://api.nabaztag.com/vl/FR/api.jsp?sn=$SERIAL&token=$TOKEN&tts=It+is+now+time+to+go+to+the+pub" 
