==============
My git aliases
==============
---------------------------------
Saving valuable keystrokes :: git
---------------------------------

Git aliases are fun time-savers.  If you use execute more than 10 git commands a
day, you should use them.  

Here's a selection from my ``.gitconfig``:

.. sourcecode:: bash
    # ~/.gitconfig

    [alias]
        ci = commit
        cn = commit --no-verify
        co = checkout
        st = status -sb
        br = branch
        df = diff
        rb = rebase
        praise = blame
        unstage = reset HEAD --
        restore = checkout --
        last = log -1 HEAD
        visualise = !gitk
        hist = log --color --pretty=format:\"%C(yellow)%h%C(reset) %C(green)%ad%C(reset) %s%C(bold red)%d%C(reset) %C(blue)[%an]%C(reset)\" --relative-date --decorate

A few things to note:

* The ``--no-verify`` option to ``git commit`` prevents the pre-commit hook from
  running.  This is useful if you have your unit test suite set up within this
  hook.  Sometimes you've just run your tests and don't need them to run again
  when you commit.

* The ``-sb`` option for ``git status`` give a concise version.  

* The ``unstage`` and ``restore`` aliases are useful for dropping changes from
  your working directory.

My favourite is ``git hist``, which shows an one-line version of ``git log``
with tags and branches included - very useful.

<image here>

However, too much time is wasted typing the 4 characters of 'git '.  Best to
use bash aliases:

.. sourcecode:: bash
    # ~/.bash_aliases

    alias git='hub'
    alias g='hub status -sb'
    alias gb='hub branch'
    alias gp='hub push'
    alias gpu='hub pull'
    alias ga='hub add'
    alias gc='hub commit'
    alias gd='hub diff'
    alias gdw='hub diff --word-diff'
    alias gh='hub hist'
    alias gl='hub log --oneline --decorate'
    alias gcv='hub commit --no-verify'

So now typing ``g`` gives a concise status.  

<image here>

I'm also using the excellent Hub
library which provides helpers for Github integration.


