=================================
A Fabric function for git tagging 
=================================
-------------------------------------------------------------------------
Using Fabric with git-flow :: git, fabric, python, deployment
-------------------------------------------------------------------------

Listed below is a `Fabric`_ function for determining the appropriate git
reference to deploy during a deployment.  It works well with projects
run using the `git-flow`_ development model.  

.. _`Fabric`: http://docs.fabfile.org/en/1.3.4/index.html
.. _`git-flow`: http://nvie.com/posts/a-successful-git-branching-model/

Set-up
------

Assume there is a test environment where:

* the QA team to assess release candidates
* developers to run integration tests
* developers can deploy 'debug' builds from a specific (untagged) commit

There will also be stage and production environments.

Fabric function
---------------

The following function can be used as part of Fabric build script.  It's purpose
is to determine the git reference to deploy from.

.. sourcecode:: python

    def determine_refspec_to_deploy_from(is_test=False)
        local('git fetch --tags')

        if is_test:
            create_tag = prompt('Tag this release? [y/N] ')
            if create_tag.lower() == 'y':
                notify("Showing latest tags for reference")
                local('git tag | sort -V | tail -5')
                refspec = prompt('Tag name [in format x.x.x]? ')
                local('git tag %(ref)s -m "Tagging version %(ref)s in fabfile"' % {
                    'ref': refspec})
                local('git push --tags')
            else:
                use_commit = prompt('Build from a specific commit? [y/N] ')
                if use_commit.lower() == 'y':
                    refspec = prompt('Choose commit to build from: ')
                else:
                    branch = local('git branch | grep "^*" | cut -d" " -f2', capture=True)
                    refspec = local('git describe %s' % branch, capture=True).strip()
        else:
            # An existing tag must be specified
            local('git tag | sort -V | tail -5')
            refspec = prompt(red('Choose tag to build from: '))

            # Check this is valid
            local('git tag | grep "%s"' % refspec)

        return refspec

Building to test
----------------

When building to test, the script allows you to:

1. Tag a release.  This is for creating release candidates for the QA team. 
2. Build without tagging.  In this case, we generate a build name using ``git
   describe``.  This is for developers who want to update the test build to run
   integration tests.
3. Build from a specific commit.  This is mainly used to dig yourself out of
   circular reference hell: when your test build emits spurious error messages
   that can't be re-created locally.  A simple bisection approach works well
   here, building from specific commits to find the commit that broke the build.

You can build to test from any branch which is often the case with git-flow,
where your next release candidate could come from ``develop`` or a release
branch ``releases/1.4``.

Building to stage and production
--------------------------------

Nothing fancy - builds to stage and production must use an existing tag to
ensure they go through the QA process.

Interesting bits
----------------

Keeping everyone in sync
~~~~~~~~~~~~~~~~~~~~~~~~

The script fetches tags at the start and, if a new one is created, pushes it
back to the remote.  This ensures that all users have access to the tagged
releases.

What's the next tag?
~~~~~~~~~~~~~~~~~~~~

This snippet shows the latest 5 tags, making it easy to determine the next tag
to use:

.. sourcecode:: bash

    git tag | sort -V | tail -5 

Constructing a build name
~~~~~~~~~~~~~~~~~~~~~~~~~

For builds to test that aren't tagged, it's still useful to give them a build
number that indicates what the latest tagged release was.  This can be done with
``git describe``, which will output something like:

.. sourcecode:: bash

    0.1.3-149-g1a48a5a

which indicates that the build came from the 149th commit after tag ``0.1.3``.