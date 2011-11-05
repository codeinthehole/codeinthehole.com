=================
Restructured blog
=================


How to publish an article
-------------------------
1.  Create an RST article file within the ``articles`` folder. 
2.  Create an article model using::

    ./manage.py local_article /path/to/article.rst
    
3.  Repeat the above steps until you are ready to publish. 
4.  Publish article using::

    ./manage.py publish_article /path/to/article.rst