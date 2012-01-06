========================================
Phing task to create an Unfuddle message
========================================
-------------------------
Sending messages :: phing
-------------------------


Another day, another new Phing task; again integrating with project management
software - this time the excellent `Unfuddle`_.

.. _Unfuddle: http://unfuddle.com/

I've been playing with Unfuddle for a few days now and it's very impressive.
You get SVN and git hosting as well as superb issue tracking. It also supports
simple project messages (which are displayed on the project dashboard) and
so-called notebooks which are essentially project wikis that can be used to
house documentation and manuals. One great feature of integrated project
management software is the ability to merge news from a variety of sources (SVN
commits, changes in ticket status, changes to notebooks) onto a single page
that provides a snapshot of the latest activity on a project. Unfuddle does
this on each project dashboard, where the latest messages are displayed along
side news of the latest SVN and issue activity. The task detailed below
provides a means for Phing to automatically add information to this dashboard
page by creating a new message.

This extension is very similar to my previous Phing task (for updating a
Twitter status), making use of the `cURL library`_ to POST XML to Unfuddle. In
this case though, the Unfuddle API for creating a message offers a few extra
options such as categorising your messages. The task supports the following
attributes:

.. _cURL library: http://uk2.php.net/curl

=============   ======= =================================================== =======     ========
Unfuddle Name   Message Description                                         Default     Required
=============   ======= =================================================== =======     ========
subdomain       String  Subdomain of Unfuddle account 
                        (eg. 'example' from http://example.unfuddle.com).   n/a         Yes
projectid       Integer Project id (eg. 123 
                        from http://example.unfuddle.com/projects/123/).    n/a         Yes
username        String  Username.                                           n/a         Yes
password        String  Password.                                           n/a         Yes
title           String  Message title.                                      n/a         Yes
body            String  Message body.                                       ''          No
categoryid      Integer The category id of the message.                     ''          No
categoryids     String  A comma-separated list of category ids (eg. 1,2,3). ''          No
checkreturn     Boolean Whether to check the return code of the request, 
                        throws a BuildException the update files.           false       No
=============   ======= =================================================== =======     ========

The only thing to note here is that you can choose whether you specify a single
category id or a collection - it wouldn't make sense to specify both these
attributes.

An example build.xml using this task would be:

.. sourcecode:: xml

    <?xml version="1.0" ?>
    <project name="Example Unfuddle update" basedir="." default="message">
        <tstamp>
            <format property="build.time" pattern="%Y-%m-%d %H:%I" />
        </tstamp>
        <taskdef name="unfuddlemessage" classname="phing.tasks.my.UnfuddleMessageTask" />
        <target name="message">
            <unfuddlemessage 
                subdomain="example" 
                projectid="12345" 
                username="exampleuser" 
                password="password" 
                title="Deploying to live site at ${build.time}" 
                body="" 
                categoryid="4" />
        </target>
    </project>

This simply creates a new Unfuddle message with the time of the last build.
This is an overly simplified example - see my previous post for a sample
parameterised deployment target that would allow a dynamic message to be
created by different targets within the deployment file.

The source code for TwitterUpdateTask.php is as follows (with docblocks
stripped out for brevity):

.. sourcecode:: php

    <?php
    require_once "phing/Task.php";
    class UnfuddleMessageTask extends Task 
    {
        const URL_TEMPLATE_UPDATE = 'http://%s.unfuddle.com/api/v1/projects/%d/messages'; 
        
        // Twitter response codes 
        const HTTP_RESPONSE_OK                  = 200;
        const HTTP_RESPONSE_CREATED             = 201;
        const HTTP_RESPONSE_BAD_REQUEST         = 400;
        const HTTP_RESPONSE_BAD_CREDENTIALS     = 401;
        const HTTP_RESPONSE_BAD_URL             = 404;
        const HTTP_RESPONSE_METHOD_NOT_ALLOWED  = 405;
        const HTTP_RESPONSE_SERVER_ERROR        = 500;
        const HTTP_RESPONSE_BAD_GATEWAY         = 502;
        const HTTP_RESPONSE_SERVICE_UNAVAILABLE = 503;

        private static $responseMessages = array(
            self::HTTP_RESPONSE_BAD_REQUEST         => 'Bad request - you may have exceeded the rate limit',
            self::HTTP_RESPONSE_BAD_CREDENTIALS     => 'Your username and password did not authenticate',
            self::HTTP_RESPONSE_BAD_URL             => 'The Unfuddle URL is invalid',
            self::HTTP_RESPONSE_METHOD_NOT_ALLOWED  => 'The specified HTTP verb is not allowed',
            self::HTTP_RESPONSE_SERVER_ERROR        => 'There is a problem with the Unfuddle server',
            self::HTTP_RESPONSE_BAD_GATEWAY         => 'Unfuddle is either down or being upgraded',
            self::HTTP_RESPONSE_SERVICE_UNAVAILABLE => 'Unfuddle servers are refusing request',
        );

        private $subdomain;
        private $projectId;
        private $username;
        private $password;
        private $title;
        private $body;
        private $categoryIds;  
        private $checkReturn = false;
        
        public function setSubdomain($subdomain) 
        {
            $this->subdomain = $subdomain;
        }
        public function setProjectId($projectId) 
        {
            $this->projectId = (int)$projectId;
        }
        public function setUsername($username) 
        {
            $this->username = $username;
        }
        public function setPassword($password) 
        {
            $this->password = $password;
        }
        public function setTitle($title) 
        {
            $this->title = $title;
        }
        public function setBody($body) 
        {
            $this->body = $body;
        }
        public function setCategoryId($categoryId) 
        {
            $this->categoryIds = array((int)$categoryId);
        }
        public function setCategoryIds($categoryIdList) 
        {
            $this->categoryIds = explode(",", $categoryIdList);
        }
        public function setCheckReturn($checkReturn)
        {
            $this->checkReturn = (boolean)$checkReturn;
        }
        
        public function init() 
        {
            if (!extension_loaded('curl')) {
                throw new BuildException("Cannot update Unfuddle", "The cURL extension is not installed");
            }
        }
        public function main() 
        {
            $this->validateProperties();
            
            $curlHandle = curl_init();
            curl_setopt($curlHandle, CURLOPT_URL, $this->getUpdateUrl());
            curl_setopt($curlHandle, CURLOPT_USERPWD, "$this->username:$this->password");
            curl_setopt($curlHandle, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($curlHandle, CURLOPT_HTTPHEADER, array('Accept: application/xml', 'Content-type: application/xml'));
            curl_setopt($curlHandle, CURLOPT_POST, true);
            curl_setopt($curlHandle, CURLOPT_POSTFIELDS, $this->getRequestBodyXml());
            $responseData = curl_exec($curlHandle);
            $responseCode = curl_getinfo($curlHandle, CURLINFO_HTTP_CODE);
            $errorCode    = curl_errno($curlHandle);
            $errorMessage = curl_error($curlHandle);
            curl_close($curlHandle);
            
            if (0 != $errorCode) {
                throw new BuildException("cURL error ($errorCode): $errorMessage");
            }
            $this->handleResponseCode((int)$responseCode);
        }
        private function validateProperties()
        {
            if (!$this->subdomain) {
                throw new BuildException("You must specify a subdomain");
            }
            if (!$this->projectId) {
                throw new BuildException("You must specify a project id");
            }
            if (!$this->username || !$this->password) {
                throw new BuildException("You must specify an Unfuddle username and password");
            }
            if (!$this->title) {
                throw new BuildException("You must specify a message title");
            }
        }
        private function getUpdateUrl()
        {
            return sprintf(self::URL_TEMPLATE_UPDATE, $this->subdomain, $this->projectId);
        }
        private function getRequestBodyXml()
        {
            $xmlWriter = new XMLWriter();
            $xmlWriter->openMemory();
            $xmlWriter->startElement('message');
            $xmlWriter->writeElement('title', $this->title);
            $xmlWriter->writeElement('body', $this->body);
            
            if ($this->categoryIds) {
                $xmlWriter->startElement('categories');
                foreach ($this->categoryIds as $categoryId) {
                    $xmlWriter->startElement('category');
                    $xmlWriter->writeAttribute('id', "$categoryId");
                    $xmlWriter->endElement();
                }
                $xmlWriter->endElement();
            }
            $xmlWriter->endElement();
            return $xmlWriter->flush();
        }
        private function handleResponseCode($code)
        {
            if ($code == self::HTTP_RESPONSE_CREATED) {
                $this->log("New Unfuddle message posted: '$this->title'", Project::MSG_INFO);
                return;
            }
            if (array_key_exists($code, self::$responseMessages)) {
                $this->handleFailedUpdate(self::$responseMessages[$code]);
            } else {
                $this->handleFailedUpdate("Unrecognised HTTP response code '$code' from Unfuddle");
            }
        }
        private function handleFailedUpdate($failureMessage)
        {
            if (true === $this->checkReturn) {
                throw new BuildException($failureMessage);
            }
            $this->log("New Unfuddle message unsuccessful: $failureMessage", Project::MSG_WARN);   
        }
    }

The fully documented source and associated example build.xml file are available
to download: `UnfuddleMessageTask.zip (2.6kb)`_

.. _UnfuddleMessageTask.zip (2.6kb): /static/downloads/UnfuddleMessageTask.zip


