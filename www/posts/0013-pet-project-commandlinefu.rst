====================================
Current pet project: Command-Line-Fu
====================================
-----------------------------------------------------
Creating a site for sharing commands :: commandlinefu
-----------------------------------------------------

.. image:: /static/images/screenshots/tomboy-commands-small.jpg
   :align: right

If you're anything like me, you spend a lot of time at the UNIX command-line
manipulating the filesystem, configuring Linux, playing with services and so
forth. As any UNIX user knows, tremendous power can be wielded through
judicious function selection, piping and output redirection. It's often quite
staggering what can be achieved in a single line given a rudimentary knowledge
of sed, grep, awk, cut…

Indeed, when I stumble upon a line of particular elegance or usefulness, I
generally log them to a `Tomboy note`_ (fired up in a flash using `Gnome-do`_). This
has proved extremely useful as I am often returning to the list to recall how
to, say, rsync a fileset with an exclude list - it's generally faster than
Googling or going to the man pages. As time has progressed though, this small
repository has grown into a sizable collection and finding a particular command
quickly is now a problem. Motivated by this problem and taking inspiration from
my daily reading (`Hacker News`_, `Programming Reddit`_ and `Stack Overflow`_), I'm in
the process of putting together a lightweight web-app for cataloguing and
ranking notable UNIX one liners.

.. _`Tomboy note`: http://projects.gnome.org/tomboy/
.. _`Gnome-do`: http://do.davebsd.com/
.. _`Hacker News`: http://news.ycombinator.com/
.. _`Programming Reddit`: http://www.reddit.com/r/programming/
.. _`Stack Overflow`: http://stackoverflow.com/

.. image:: /static/images/screenshots/clf-small.jpg
   :align: right
   :target: http://www.commandlinefu.com

The basic idea is for users to be able to store their useful one liners on the
site for (a) retrieval in the future and (b) sharing with others who
undoubtedly will need to save the same problem. Once created, these commands
are parsed for the functions used and any relevant tags to provide good
navigational props. The individual commands also be discussed and commented on.
Further, users can vote on each others commands allowing simple leaderboards to
be constructed. After a few months, it will be interesting to see what the top
10 most useful awk commands are.

It's only been a week (working piecemeal after dinner) but the site's nearly
ready for a beta release. It's constructed using a combination of CodeIgniter
and Zend Framework, making use of the fast and lightweight nature of
CodeIgniter coupled with the extensive range of components that ZF provides.
The site's called http://www.commandlinefu.com and should be live in about a
week assuming I find some spare time over the weekend. Watch this space.
