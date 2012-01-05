================
Another RST blog
================

Process for writing a new article is now:

1. Activate virtualenv (using ``virtualenvwrapper`` with a customised ``bin/activate`` to change 
   directory)

2. Create RST article file::

    vim posts/my-new-article.rst

3. Check article locally::

    ./manage.py rsb_article posts/my-new-article.rst
    ./manage.py runserver

4. When happy, publish::

   fab prod publish posts/0036-my-new-article.rst

This last step copies the RST file up to the remote server and runs::

    ./manage.py rsb_article --publish posts/my-new-article.rst


Must-have:
* Articles written in RST, converted to HTML
* Good code highlighting
* RSS feed
* Simple tagging


    
