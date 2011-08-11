Todo
====

Single article page
Show snippets on homepage


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
* Article page - links to previous and next articles

Design
======

* Center justified, 70 chars wide

Process
=======

* Create local ``.rst`` file in articles folder
* Run ``./manage.py local_article articles/sample.rst`` to create/update a DB entry
  for this article.
* Run ``./manage.py publish_article articles/sample.rst`` to publish article to remote server.  This






