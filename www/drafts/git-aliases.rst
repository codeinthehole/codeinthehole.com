==============================
Git aliases for fun and profit
==============================

The following are useful:

.. sourcecode:: bash
    
    ...
    [alias]
        ci = commit
        co = checkout
        st = status
        br = branch
        praise = blame
        unstage = reset HEAD --
        restore = checkout --
        last = log -1 HEAD
        visualise = !gitk
        hist = log --pretty=format:\"%h %ad | %s%d [%an]\" --date=short



