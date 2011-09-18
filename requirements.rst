Todo
====

- Rename to rsb
- Upload to github
- Don't show bio on non-article pages


- Homepage
    * Photo
    * Blurb
    * Projects
    * Github
    * Twitter 
    * Stack Overflow 
    * Shelfari
    
- Latex tutorial
- CGL tutorial

- Redirects from old site - give them the same PKs to make lookups easier

- Write up latex tutorial as article

* Single article page
    - Related articles
    
* Show snippets on homepage
* Get python highlighted correctly
* Long code lines?
* Next and prevoius articles
TAgging articles
RSS feeds

* Split project into library and project


Requirements
============

Must-have:
* Articles written in RST, converted to HTML
* Good code highlighting
* RSS feed
* Simple tagging

Nice-to-have:
* Github/gist integration
  
Pages
=====

* Homepage - extended snippet of first article, short snippets of 4 more
  - some intro text and links to github etc
* Blog page - Extended snippet of most recent 5 articles and shorter
  shippets of next 5.
* Article page - links to previous and next articles
* About page


To copy
=======
http://hawksworx.com/blog/
http://kev.inburke.com/kevin/site-redesign/
http://zachholman.com/

Design
======

* Center justified, 70 chars wide

Process
=======

* Create local ``.rst`` file in articles folder
* Run ``./manage.py local_article articles/sample.rst`` to create/update a DB entry
  for this article.
* Run ``./manage.py publish_article articles/sample.rst`` to publish article to remote server.  This






