========================================
How to set-up MySQL for Python on Ubuntu
========================================
------------------------------------------------------
This doesn't stick in my head :: python, mysql, ubuntu
------------------------------------------------------

This is just for my own reference as I always forget the dependencies for setting up MySQL
on a new machine.

Installation
------------

Starting with a vanilla Lucid install [#]_, install pip and upgrade to
the latest version:

.. sourcecode:: bash

    apt-get install python-pip
    pip install -U pip

Next, install the required development packages:

.. sourcecode:: bash

    apt-get install python-dev libmysqlclient-dev

then

.. sourcecode:: bash

    pip install MySQL-python

should complete successfully.

.. [#] Tested using the Lucid32 Vagrant box: http://files.vagrantup.com/lucid32.box

Symptoms of missing headers
---------------------------

Without ``libmysqlclient-dev``, you'll see something like this:

.. sourcecode:: bash

    Downloading/unpacking MySQL-python
    Running setup.py egg_info for package MySQL-python
        sh: mysql_config: not found
        Traceback (most recent call last):
        File "<string>", line 14, in <module>
        File "/home/vagrant/build/MySQL-python/setup.py", line 15, in <module>
            metadata, options = get_config()
        File "setup_posix.py", line 43, in get_config
            libs = mysql_config("libs_r")
        File "setup_posix.py", line 24, in mysql_config
            raise EnvironmentError("%s not found" % (mysql_config.path,))
        EnvironmentError: mysql_config not found
        Complete output from command python setup.py egg_info:
        sh: mysql_config: not found

    Traceback (most recent call last):

    File "<string>", line 14, in <module>

    File "/home/vagrant/build/MySQL-python/setup.py", line 15, in <module>

        metadata, options = get_config()

    File "setup_posix.py", line 43, in get_config

        libs = mysql_config("libs_r")

    File "setup_posix.py", line 24, in mysql_config

        raise EnvironmentError("%s not found" % (mysql_config.path,))

    EnvironmentError: mysql_config not found


Without ``python-dev``, you'll see something that ends with the following:

.. sourcecode:: bash

    ...

        _mysql.c:2620: error: expected '=', ',', ';', 'asm' or '__attribute__' before '_mysql_ResultObject_Type'

    _mysql.c:2706: error: expected '=', ',', ';', 'asm' or '__attribute__' before '_mysql_methods'

    _mysql.c:2778: error: expected '=', ',', ';', 'asm' or '__attribute__' before '*' token

    _mysql.c:2810: warning: return type defaults to 'int'

    _mysql.c: In function 'DL_EXPORT':

    _mysql.c:2810: error: expected declaration specifiers before 'init_mysql'

    _mysql.c:2888: error: expected '{' at end of input

    error: command 'gcc' failed with exit status 1

    ----------------------------------------
    Command /usr/bin/python -c "import setuptools;__file__='/home/vagrant/build/MySQL-python/setup.py';exec(compile(open(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --single-version-externally-managed --record /tmp/pip-dPF1DK-record/install-record.txt failed with error code 1
    Storing complete log in /home/vagrant/.pip/pip.log