=================================
An SSH tip for modern AWS patrons
=================================
--------------------------------------------------------
Slightly useful tip for SSHing onto EC2 instances :: aws
--------------------------------------------------------

Cloud computing and immutable infrastructure deployments have changed the way I
use SSH. I miss the days when I could run:

.. sourcecode:: bash

    $ ssh app1-prod

to jump onto a machine and investigate an issue. This would work as,
back in the days of yore, your web servers didn't change IP address
several times a week so I could create a helpful alias in ``~/.ssh/config``:

.. sourcecode:: ssh

    Host app1-prod
        User example_user
        HostName 74.207.251.29

This circumvented the labour-intensive act of typing in the remote username and
IP address when SSHing around town.

I can no longer do this as:

- Immutable infrastructure deployments mean EC2 instances are replaced for
  every update so the IP addresses keep changing.  Life is too short to keep
  updating ``~/.ssh/config`` with their details.

- Plus, aside from your load balancers, servers should be unreachable from the
  outside world. Now all access is via a bastion machine: the only machine in
  the VPC that exposes its SSH port to the network your laptop is using.

These are both good things.

Aren't you supposed to stop using SSH with AWS?
-----------------------------------------------

Yeah, `that's been recommended before`_ and seems a good idea.

.. _`that's been recommended before`: https://wblinks.com/notes/aws-tips-i-wish-id-known-before-i-started/

I'm not there yet though. There's still occasions where I want to SSH onto
a machine and run diagnostics.  For instance, as part of a
`canary release`_ I often SSH onto one of the new machines and check
for smoke before replacing the entire auto-scale group with the new 
AMI. (I'm happy to accept this is an regrettable practice and I need to raise my
automation game.)

.. _`canary release`: http://martinfowler.com/bliki/CanaryRelease.html

In such circumstances, I want to be able to run:

.. sourcecode:: bash

    $ ssh ip-10-5-8-179.eu-west-1.compute.internal

jumping straight onto an AWS EC2 instance using only its internal DNS name,
plucked from the AWS console or a ``boto`` command.

Here's how.

ProxyCommand and a wildcard SSH alias
-------------------------------------

Add an alias to ``~/.ssh/config`` for your bastion server. Something like:

.. sourcecode:: ssh

    Host bastion-prod
        User example_user
        Hostname bastion.example.com
        IdentityFile ~/.ssh/bastion-prod.key
        LogLevel Quiet

then you can route SSH traffic through the bastion server using ``ProxyCommand``: 

.. sourcecode:: ssh

    Host *.compute.internal
        User ubuntu
        IdentityFile ~/.ssh/aws-prod.key
        ProxyCommand ssh bastion-prod -W %h:%p
        StrictHostKeyChecking no

and that's sufficient for commands like:

.. sourcecode:: bash

    $ ssh ip-10-5-8-179.eu-west-1.compute.internal

to work.

Note, disabling ``StrictHostKeyChecking`` suppresses the confirmation prompt when
connecting to a new host for the first time. I'm ignorant of whether this is a
dreadful security misstep.

Some vaguely related articles:

- `Using a ProxyCommand to Leap Frog Your Bastions`_
- A `Github repo`_ for dynamically building ``~/.ssh/config`` using boto.
- `Easily SSH into Amazon EC2 instances using the Name tag`_

.. _`Using a ProxyCommand to Leap Frog Your Bastions`: http://edgeofsanity.net/article/2012/10/15/ssh-leap-frog.html
.. _`Github repo`: https://github.com/gianlucaborello/aws-ssh-config
.. _`Easily SSH into Amazon EC2 instances using the Name tag`: http://blog.ryanparman.com/2014/01/29/easily-ssh-into-amazon-ec2-instances-using-the-name-tag/
