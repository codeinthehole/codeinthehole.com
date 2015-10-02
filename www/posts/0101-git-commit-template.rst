=====================================
A useful template for commit messages
=====================================
-------------------------------------------------------------
A simple heuristic for preferring the imperative mood :: git 
-------------------------------------------------------------

Here's a useful heuristic for writing better commit messages. Set your commit
message template to:

.. sourcecode:: text

    # If applied, this commit will...

    # Why is this change being made?

    # Provide links to any relevant tickets, URLs or other resources

and you'll be guided into writing concise commit subjects in the imperative
mood - a good practice.  See rule 5 of Chris Beam's `"How to write a commit message"`_ 
for the inspiration of this tip and more reasoning on the use of the imperative
mood.

To do this in Git, save the above content in a file (eg
``~/.git_commit_msg.txt``) and run:

.. sourcecode:: bash

    $ git config —global commit.template ~/.git_commit_msg.txt

Here's what this looks like in practice:

.. image:: /static/images/git-commit-snap.png
    :width: 800px

.. _`"How to write a commit message"`: http://chris.beams.io/posts/git-commit/


