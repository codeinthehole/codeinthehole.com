=================================================================================
The most important command-line tip - incremental history searching with .inputrc
=================================================================================
-----------------------------------------------------------
Big productivity boost from using readline :: commandlinefu
-----------------------------------------------------------

Getting www.commandlinefu.com off the ground has renewed my interest in Bash,
UNIX and all things command-line. Powerful one-liners are things of beauty and
are worth collecting; however what I consider to be the most influential
command-line tip I know covers four:

.. sourcecode:: bash

    "\e[A": history-search-backward
    "\e[B": history-search-forward
    "\e[C": forward-char
    "\e[D": backward-char

These lines need to be placed in your ``~/.inputrc`` file, the start-up script for
the Readline utility used by Bash (as well as several other applications) and
others). The important commands here are the first two, which bind your up and
down cursor keys to incrementally search your history. (The second two ensure
that left and right continue to work correctly).

This is *incredibly useful* for retrieving commands you've used previously and
makes a huge difference to your productivity. For instance, to find a previous
SSH command from a few days ago, simply type "ss" and press up a few times.
This will allow you to browse through all your previous ssh… commands until you
find the right one - you never need to use more than 4 or 5 keystrokes to
retrieve any previous command. If your cycling through too many commands to
find the right one, type in a few more characters to refine the search.

As indicated above, this functionality is available in all applications that
use Readline including MySQL, Python, IRB (interactive Ruby shell) and others.
Once you're used to this feature, it's hard to live without - the first thing I
do once I've been set up as a user on a new server is update my .inputrc file
to contain these settings. The one place where I sorely wish this functionality
existed is the Firebug Javascript commandline in Firefox (a ticket already
exists requesting a similar feature).

Another way of searching your history is to use CTRL+R, which essentially
performs a full-text search on your history (keep pressing CTRL+R to cycle
through results). In this case, searching for "ssh" will locate all commands
that feature this string anywhere in the command. Although this is actually a
more powerful feature than the incremental history search described above, I
don't often use it as: (a) the incremental search generally lets me jump to the
desired command in fewer key-presses and (b) I find "ssh", CTRL+R, CTRL+R
slightly awkward to type and less intuitive than "ssh", UP, UP. Horses for
courses really - you could probably be just as efficient with either one.

» Hat-tip to the place where I first learnt this: `Power Shell Usage`_ by Simon
Myers

.. _Power Shell Usage: http://www.ukuug.org/events/linux2003/papers/bash_tips/

One extra thing: this functionality can be neatly complimented by some choice
history settings in your ``~/.bashrc`` file:

.. sourcecode:: bash

    export HISTSIZE=1000000
    export HISTFILESIZE=1000000000

These simply set your history to be very large so that you have a huge bank of
commands to search.
