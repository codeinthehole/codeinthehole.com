=========================================
How to install PIL on 64-bit Ubuntu 12.04
=========================================
----------------------------------------------------------------
Because I have to look this up every time :: python, pil, ubuntu
----------------------------------------------------------------

Problem
-------

You want to install PIL on 64-bit Ubuntu 12.04 (Precise Pangolin).  

Solution
--------

With pip already installed, install the required development packages:

.. sourcecode:: bash
    
    $ sudo apt-get install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev

and symlink the three image libraries into ``/usr/lib``:

.. sourcecode:: bash

    $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
    $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
    $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/

PIL should now install with support for JPEGs, PNGs and FreeType, as indicated
by the compilation output:

.. sourcecode:: bash

    --------------------------------------------------------------------
    PIL 1.1.7 SETUP SUMMARY
    --------------------------------------------------------------------
    version       1.1.7
    platform      linux2 2.7.3 (default, Apr 20 2012, 22:39:59)
                  [GCC 4.6.3]
    --------------------------------------------------------------------
    *** TKINTER support not available
    --- JPEG support available
    --- ZLIB (PNG/ZIP) support available
    --- FREETYPE2 support available
    *** LITTLECMS support not available
    --------------------------------------------------------------------

Common problems
---------------

Missing image libraries
~~~~~~~~~~~~~~~~~~~~~~~

If the image libraries are not installed and available in ``/usr/lib``, you'll
see something like this:

.. sourcecode:: bash

    --------------------------------------------------------------------
    PIL 1.1.7 SETUP SUMMARY
    --------------------------------------------------------------------
    version       1.1.7
    platform      linux2 2.7.3 (default, Apr 20 2012, 22:39:59)
                  [GCC 4.6.3]
    --------------------------------------------------------------------
    *** TKINTER support not available
    *** JPEG support not available
    *** ZLIB (PNG/ZIP) support not available
    *** FREETYPE2 support not available
    *** LITTLECMS support not available
    --------------------------------------------------------------------
    To add a missing option, make sure you have the required
    library, and set the corresponding ROOT variable in the
    setup.py script.

Missing python headers
~~~~~~~~~~~~~~~~~~~~~~

Without ``python-dev``, you'll see something that ends with the following:

.. sourcecode:: bash

    ...

    running build_ext

    building '_imaging' extension

    creating build/temp.linux-x86_64-2.7

    creating build/temp.linux-x86_64-2.7/libImaging

    gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -IlibImaging -I/usr/include -I/usr/local/include -I/usr/include/python2.7 -c _imaging.c -o build/temp.linux-x86_64-2.7/_imaging.o

    _imaging.c:75:20: fatal error: Python.h: No such file or directory

    compilation terminated.

    error: command 'gcc' failed with exit status 1

Discussion
----------

Yes, this has been written about before.  This is just my note-to-self that
I can refer others to - I also wanted to include the common error messages that
people will search for.  

* `Installing PIL in a virtualenv on Ubuntu 12.04 Precise Pangolin`_
* `Install PIL with JPEG support on Ubuntu Oneric 64bit`_
* `How to install PIL on Ubuntu`_

.. _`Installing PIL in a virtualenv on Ubuntu 12.04 Precise Pangolin`: http://www.sandersnewmedia.com/why/2012/04/16/installing-pil-virtualenv-ubuntu-1204-precise-pangolin/ 
.. _`Install PIL with JPEG support on Ubuntu Oneric 64bit`: http://jj.isgeek.net/2011/09/install-pil-with-jpeg-support-on-ubuntu-oneiric-64bits/
.. _`How to install PIL on Ubuntu`: http://www.saltycrane.com/blog/2010/10/how-install-pil-ubuntu/

