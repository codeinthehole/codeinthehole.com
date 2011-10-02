===================================
Phing task to update Twitter status
===================================
--------------------------------------------------------------------
Simple PHP extension to Phing for Tweeting :: phing, deployment, php
--------------------------------------------------------------------

At Tangent Labs, we're currently experimenting with integrating Twitter into
our project workflow to provide a latest activity feed in a easily digestible
format (for both developers and non-technical people). For a pilot project,
we've created a Twitter account and added an SVN post-commit hook script that
updates Twitter with the latest commit information (commit message, affected
files, author). We're going to integrate our bug-tracking software shortly too
but that's not the subject of this post.

Instead, I'm going to detail a custom Phing task I've written that updates the
project Twitter account. This allows notices of builds (to test, stage and
production) to be integrated into a single feed. One of the great things about
Twitter is its API and the range of applications already written to interact
with it. My current favourite client is Gwibber, which (amongst other things)
displays a small pop-up whenever the account gets a new update. Having this
running while working on the project is great for staying informed with the
latest activity, be it new commits, opened tickets or deployments.

The task I've written is TwitterUpdateTask.php and should be copied into your
``$PATH_TO_PHING/ext/my/`` folder (create it if it doesn't exist already).
Mirroring the format of the Phing docs, this task has the following attributes:

============    =======  ========================================   =======    ========
Name            Type     Description                                Default    Required
============    =======  ========================================   =======    ========
username        String   Twitter username                           n/a        Yes
password        String   Twitter password                           n/a        Yes
message         String   Update message                             n/a        Yes
checkreturn     Boolean  Whether to check the request return code   false      No  
============    =======  ========================================   =======    ========

A simple example build.xml file using this task is as follows:

.. sourcecode:: xml

    <?xml version="1.0" ?>
    <project name="Simple Twitter update" basedir="." default="tweet">
        <tstamp>
            <format property="build.time" pattern="%Y-%m-%d %H:%I" />
        </tstamp>
        <taskdef name="twitterupdate" classname="phing.tasks.my.TwitterUpdateTask" />
        <target name="tweet">
            <twitterupdate 
                username="example" password="mypassword" 
                message="Build at ${build.time}" />
        </target>
    </project>

This simply updates the Twitter status with the time of the last build. A more
useful means of using this task is to parameterise the Twitter target to take a
specified message so that it can be called from different deployment targets:

.. sourcecode:: xml

    <?xml version="1.0" ?>
    <project name="Example Twitter update" basedir="." default="deploy-to-test">
        <tstamp>
            <format property="build.time" pattern="%Y-%m-%d %H:%I" />
        </tstamp>
        <taskdef name="twitterupdate" classname="phing.tasks.my.TwitterUpdateTask" />
        <target name="tweet">
            <twitterupdate 
                username="dave_test" password="eggnog" 
                message="${twitter.status}" />
        </target>
        <target name="deploy-to-test">
            <phingcall target="tweet">
                <property 
                    name="twitter.status" 
                    value="Deploying to test: ${build.time}" />
            </phingcall>
        </target>
        <target name="deploy-to-stage">
            <phingcall target="tweet">
                <property 
                    name="twitter.status" 
                    value="Deploying to stage: ${build.time}" />
            </phingcall>
        </target>
        <target name="deploy-to-production">
            <phingcall target="tweet">
                <property 
                    name="twitter.status" 
                    value="Deploying to production: ${build.time}" />
            </phingcall>
        </target>
    </project>

There are lots of extensions from this idea such as updating Twitter with
continuous integration results, failed builds, code coverage metrics.

The source code for TwitterUpdateTask.php is as follows (with docblocks
stripped out for brevity):

.. sourcecode:: php

    <?php
    require_once "phing/Task.php";
    class TwitterUpdateTask extends Task 
    {
        const URL_TEMPLATE_UPDATE    = 'http://twitter.com/statuses/update.xml?status=%s'; 
        const MAXIMUM_MESSAGE_LENGTH = 140;
        
        // Twitter response codes 
        const HTTP_RESPONSE_SUCCESS             = 200;
        const HTTP_RESPONSE_NOT_MODIFIED        = 304;
        const HTTP_RESPONSE_BAD_REQUEST         = 400;
        const HTTP_RESPONSE_BAD_CREDENTIALS     = 401;
        const HTTP_RESPONSE_FORBIDDEN           = 403;
        const HTTP_RESPONSE_BAD_URL             = 404;
        const HTTP_RESPONSE_SERVER_ERROR        = 500;
        const HTTP_RESPONSE_BAD_GATEWAY         = 502;
        const HTTP_RESPONSE_SERVICE_UNAVAILABLE = 503;
        
        private static $responseMessages = array(
            self::HTTP_RESPONSE_NOT_MODIFIED        => 'Status hasn\'t changed since last update',
            self::HTTP_RESPONSE_BAD_REQUEST         => 'Bad request - you may have exceeded the rate limit',
            self::HTTP_RESPONSE_BAD_CREDENTIALS     => 'Your username and password did not authenticate',
            self::HTTP_RESPONSE_FORBIDDEN           => 'Forbidden request - Twitter are refusing to honour the request',
            self::HTTP_RESPONSE_BAD_URL             => 'The Twitter URL is invalid',
            self::HTTP_RESPONSE_SERVER_ERROR        => 'There is a problem with the Twitter server',
            self::HTTP_RESPONSE_BAD_GATEWAY         => 'Twitter is either down or being upgraded',
            self::HTTP_RESPONSE_SERVICE_UNAVAILABLE => 'Twitter servers are overloaded and refusing request',
        );
        
        private $username;
        private $password;
        private $message;
        private $checkReturn = false;
        
        public function setUsername($username) {
            $this->username = $username;
        }
        public function setPassword($password) {
            $this->password = $password;
        }
        public function setMessage($message) 
        {
            $this->message = trim($message);
        }   
        public function setCheckReturn($checkReturn)
        {
            $this->checkReturn = (boolean)$checkReturn;
        }
        public function init() 
        {
            if (!extension_loaded('curl')) {
                throw new BuildException("Cannot update Twitter", "The cURL extension is not installed");
            }
        }
        public function main() 
        {
            $this->validateProperties();       
            $curlHandle = curl_init();
            curl_setopt($curlHandle, CURLOPT_POST, true);
            curl_setopt($curlHandle, CURLOPT_POSTFIELDS, array());
            curl_setopt($curlHandle, CURLOPT_URL, $this->getUpdateUrl());
            curl_setopt($curlHandle, CURLOPT_USERPWD, "$this->username:$this->password");
            curl_setopt($curlHandle, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($curlHandle, CURLOPT_HTTPHEADER, array('Expect:'));
            $twitterData  = curl_exec($curlHandle);
            $responseCode = curl_getinfo($curlHandle, CURLINFO_HTTP_CODE);
            $errorCode    = curl_errno($curlHandle);
            $errorMessage = curl_error($curlHandle);
            curl_close($curlHandle);       
            if (0 != $errorCode) {
                throw new BuildException("cURL error ($errorCode): $errorMessage");
            }
            $this->handleTwitterResponseCode((int)$responseCode);
        }
        private function validateProperties()
        {
            if (!$this->username || !$this->password) {
                throw new BuildException("You must specify a Twitter username and password");
            }
            if (!$this->message) {
                throw new BuildException("You must specify a message");
            } elseif (strlen($this->message) > self::MAXIMUM_MESSAGE_LENGTH) {
                $this->message = substr($this->message, 0, self::MAXIMUM_MESSAGE_LENGTH);
                $this->log("Message is greater than the maximum message length - truncating...", Project::MSG_WARN);
            }
        }    
        private function getUpdateUrl()
        {
            return sprintf(self::URL_TEMPLATE_UPDATE, $this->getEncodedMessage());
        }   
        private function getEncodedMessage()
        {
            return urlencode(stripslashes(urldecode($this->message)));
        }  
        private function handleTwitterResponseCode($code)
        {
            if ($code == self::HTTP_RESPONSE_SUCCESS) {
                $this->log("Twitter status updated to: '$this->message'", Project::MSG_INFO);
                return;
            }
            if (array_key_exists($code, self::$responseMessages)) {
                $this->handleFailedUpdate(self::$responseMessages[$code]);
            } else {
                $this->handleFailedUpdate("Unrecognised HTTP response code '$code' from Twitter");
            }
        }   
        private function handleFailedUpdate($failureMessage)
        {
            if (true === $this->checkReturn) {
                throw new BuildException($failureMessage);
            }
            $this->log("Update unsuccessful: $failureMessage", Project::MSG_WARN);   
        }
    }
 
The fully documented source and associated example build.xml file are available
to download:

» TwitterUpdateTask.zip (2.6kb)
