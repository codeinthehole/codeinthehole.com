==============================
Git aliases for fun and profit
==============================
---------------------------------
Saving valuable keystrokes :: git
---------------------------------

Git aliases are fun.  Here's a selection from my ``.gitconfig``:

.. sourcecode:: bash

    [alias]
        ci = commit
        cn = commit --no-verify
        cm = commit -m
        co = checkout
        st = status
        br = branch
        df = diff
        rb = rebase
        praise = blame
        unstage = reset HEAD --
        restore = checkout --
        last = log -1 HEAD
        visualise = !gitk
        hist = log --pretty=format:\"%h %ad | %s%d [%an]\" --date=short

