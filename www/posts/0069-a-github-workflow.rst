===========================================
Converting Github issues into pull requests
===========================================
----------------------------------
A better workflow using Hub :: git
----------------------------------

Using the Hub_ library, it's possible to convert Github issues into pull
requests.  This gives rise to a useful Github workflow which this article
describes.

.. _Hub: http://defunkt.io/hub/

This is nothing new; it's been `written about before`_.  However, this is something
I do all the time whilst developing Oscar_ and I'm fed up with explaining it.
This article is a reference I can point people at.  

.. _Oscar: https://github.com/tangentlabs/django-oscar
.. _`written about before`: http://www.topbug.net/blog/2012/03/25/attach-a-pull-request-to-an-existing-github-issue/

Workflow
========

Discuss
-------

Discuss an idea for a new feature on the project mailing list.  Agree
on what needs to be done.

Specify
-------

Create a Github issue for the feature.  

It's often useful to write the ticket as a brief functional spec, documenting
the requirements as user stories.  Github's `support for checkboxes in markdown`_ is
useful here:

.. _`support for checkboxes in markdown`: https://github.com/blog/1375-task-lists-in-gfm-issues-pulls-comments

Work
----

Create a feature branch to work on this issue:

.. sourcecode:: bash

    (master) $ git checkout -b issue/472/django1.5

I find it helpful to include the issue number in the branch name but that might
not be to your taste.

Work and commit onto your branch as normal.

Review
------

Now push to the remote:

.. sourcecode:: bash

    (issue/472/django1.5) $ git push -u origin issue/472/django1.5

and attach your commits to the original issue, thereby converting it
into a pull request.

.. sourcecode:: bash

    (issue/472/django1.5) $ hub pull-request -i 472 -h tangentlabs:issue/472/django1.5

where ``tangentlabs`` is the Github username of the owner of the ``origin`` remote.

Note the issue branch was pushed to the ``origin`` remote rather than a fork.
This is convenient as it lets other developers add commits to the pull request.

Iterate
-------

The pull request can now be code-reviewed and further commits added.  This
process continues until the issue is resolved and can be merged into ``master``.

Notes
=====

Hub's ``pull-request`` command is useful yet relatively unknown. The ``-i`` flag
indicates the Github issue number while ``-h`` specifies the source branch for
the pull request.  Here's the relevant help snippet::

    git pull-request [-f] [TITLE|-i ISSUE|ISSUE-URL] [-b BASE] [-h HEAD]
           Opens a pull request on GitHub for the project that the "origin"
           remote points to. The default head of the pull  request  is  the
           current  branch.  Both  base and head of the pull request can be
           explicitly given in one  of  the  following  formats:  "branch",
           "owner:branch",  "owner/repo:branch".  This  command  will abort
           operation if it detects that the current topic branch has  local
           commits  that  are  not yet pushed to its upstream branch on the
           remote. To skip this check, use -f.

           If TITLE is omitted, a text editor will open in which title  and
           body  of  the  pull request can be entered in the same manner as
           git commit message.

           If instead of normal TITLE an issue number is given with -i, the
           pull  request  will  be  attached  to  an existing GitHub issue.
           Alternatively, instead of title you can paste a full URL  to  an
           issue on GitHub.

Without this command, you would end up creating a separate pull-request and
issue for the same piece of work.

You can see this workflow in action via `Oscar's pull requests`_.

.. _`Oscar's pull requests`: https://github.com/tangentlabs/django-oscar/pulls
