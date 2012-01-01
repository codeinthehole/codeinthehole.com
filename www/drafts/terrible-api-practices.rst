======================
Terrible API practices
======================

Just off the back of a major project, working with several external partners.


Dreadful APIs I've had to integrate with:




Integrating with the API requires you to:

* Run their custom ``.jar`` file to generate checksums for signing requests.
* Run their ``.pyc`` files as they insist on obfuscating the code that talks 
  to their own API.  Alledgedly, the reverse engineering their code is "illegal".
* Having to submit all data to them in an auto-submitting form so it is POSTed from
  the customer's browser.
* Having per-app-server credentials - all app servers should be identical
* Having to hook into the restart of webserver event 

