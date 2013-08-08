================================
Enhancing your git commit editor
================================
---------------------------------------------------
Commit message pedantry taken to a new level :: git
---------------------------------------------------

Confession: I am a pedant, especially around commit messages.

I often find myself writing very similar commit messages (like "Bump version to
0.4.3") and want to ensure I use the same wording each time.  Thanks to
`@LuRsT`_, I learnt how to employ git's prepare-commit-msg_ hook to display
the last 5 commit messages when I'm editing a commit message.

Use the following ``.git/hooks/prepre-commit-msg`` hook:

.. sourcecode:: bash

    #!/bin/sh

    echo "#"
    echo "# Last 5 commit messages" >> $1
    echo "# ----------------------" >> $1
    COMMITS=`git log --pretty=format:"# %h %s [%an]" -5`
    echo "${COMMITS}" >> $1

then your default commit template looks like this:

.. image:: /static/images/screenshots/git-commit-editor.png

Note, using ``echo "${COMMITS}"`` (instead of ``echo $COMMITS``) ensures newlines are preserved (which I learnt in
`this Stack Overflow answer`_)

.. _`@LuRsT`: https://twitter.com/LuRsT
.. _prepare-commit-msg: http://git-scm.com/book/en/Customizing-Git-Git-Hooks#Client-Side-Hooks
.. _`this Stack Overflow answer`: http://stackoverflow.com/questions/754395/losing-newline-after-assigning-grep-result-to-a-shell-variable
