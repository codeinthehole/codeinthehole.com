=========================================================
Multi-scp: copying a file to all hosts in your SSH config
=========================================================
----------------------------------------------------------------
Using node.js to copy a file to multiple remote hosts :: node.js
----------------------------------------------------------------

I am totally reliant on my bash aliases and readline configuration. When
working on a new server, the first thing I do is copy over my local Bash
(``~/.bashrc``) and Readline (``~/.inputrc``) configuration files.

One mildly annoying issue is when you update a config file, it's a pain to copy
it onto all your remote hosts. To scratch this itch, I wrote a simple node.js
executable for copying a file to all the defined hosts in your ``~/.ssh/config``
file

Usage is trivial:

.. sourcecode:: bash

    $ multi-scp ~/.bashrc
    Starting sync of '~/.bashrc' to all hosts in /home/david/.ssh/config
    -> Copying to mars
    -> Copying to venus
    -> Copying to jupiter
    <- Successful copy to mars
    <- Successful copy to venus
    <- Successful copy to jupiter

Using node.js seems an odd choice as this could trivially be done in another
scripting language. However, I wanted to use node as:

* it allows the copy operation to run asynchronously in a child process with a callback to handle completion and error;
* it's fashionable.

The `code is on Github`_ as usual. 

.. _`code is on Github`: https://github.com/codeinthehole/node-multi-scp