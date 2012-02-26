=============
PHP to Python
=============

Abstract:

Many programmers cut their teeth with PHP before getting interested in Python.
However, while the languages seem similar at first, there are many new concepts
to grasp and new ecosystem of tools to master. This isn't easy, but with the
right advice, a strong PHP developer can become an excellent Python developer
very quickly.

Based on the experience of migrating a 20-person development team from PHP to
Python and Django, this talk will examine how to tackle this journey. While the
fundamental languages differences will be touched upon, this talk will focus on
more interesting topics such as common python gotchas, tips for grokking
Django, awesome tools and applications from the community, and how to manage
such a migration for a large team of developers.

Credits for photos
http://www.colourlovers.com/palette/871636/A_Dream_in_Color


Slides
======

Title
Tangent background - why I am qualified
What the talk is - eg not a python tutorial
-> Python's personality - what they don't say in the tutorial

What's gone:
- syntactical cruft
- privacy (consenting adults and all that)
- Java: type-hinting, interfaces, 
- other stuff
    - no switch statement
    - no ternary operators

What you'll miss:
- var_dump
- trivial server set-up
- erm, that's it..

What's different: 
- really small core
- type conversion - only numbers do this
- no arrays -> lots of data-structures
- multiple inheritance
- project layout - more than one class per file

Gotchas:
- integer division
- Mutable defaults
- no implicit copying
- no delarations of instance attributes
- catchgin multiple exceptions
- circular reference problems - cryptic error messages

What's good?
- interpreter/ipython
- language features:
  - list comprehensions
  - iterators/generators
- pdb
- pip / ecosystem
    - virtualenv
    - testing tools: mock, pyhamcrest, nose, twill, 
    - celery
    - fabric
    - Django -> next section

Django:
- admin interface
- class-based views
- django_extensions
- south, debug toolbar, sentry

Teams/migration:
- books
- sharing: pairing / talks / code-review

Tips:
- do a pure python project as well as a django one
- make sure you get your IDE set-up properly
- read the stdlib source

Summary:
- no-one regrets moving to python
- stuff still vaguely fashionable (on hacker news)






Everthing is an object

Notes
=====

Structure:
- why, background, etc
- language differences of note
- gotchas
  testing: nose, mock
- django - django_extensions, django_nose, django_celery
           south 
- teams

- not here to bash PHP - used it for ages - would defend it

Language differences:

- multiple inheritance - mixins
- less java like (private methods) - can reach into anywhere and change things
- Iterators, generators
- Indexing raises Unit testing needed - less forgiving
- Design by committee vs BDFL
- Exceptions -> TDD
- Consenting adults - PHP tries to protect the world from PHP devs
- Slightly higher learning curve with PHP
- Missing: switch, ternary operators, god-array
- OO : abstract,final,private

What people found difficult;
- Switching away from print statements to using a dbugger (eg no var_dump)
- Logging very complicated
- New datastructures
- Difference between django and python
- Strong typing - less forgiving
- Getting your editor set-up for virtualenv
- Interpretting error messages

Tips:
- Do a pure python project
- Read the stdlib


- Setting up a real server is more difficult than with PHP

Found useful:
Django/python docs
help(), dir(), ipython

Now love:
- not just a scripting language
- list comprehensions, generators, file handling
- map, enumerate, sets

You'll need to get used to:
- significant whitespace
- more than one class per file
- modules! (eg no need for static functions)
- no constants
- no privacy

PHP is thin wrapper around C libraries, inconsistent APIs
PHP is more easy-going.  Everything set to Null by default, referencing
undefined var is error but not in PHP
cleaner, more concise
More sophisticated object features: metaclassses, descriptors
context managers

Eco-system:
- pip, PyPi, github
- read the source / read github / look how other people do things
- python packages / crate.io
- more stuff on hacker new / reddit
- virtualenv, pip freeze, post-activate

Tools:
- testing
- ipython, REPL, pdb

Django:
- debug toolbar
- django_extensions
- south
- celery

gotchas:
return super
now passing args, kwargs
handling DoesNotExist,...

update-project.sh
pre-commit.sh

Security:
we got pen-tested
enumeration bugs

http://agiliq.com/books/djangogotchas/

Learn all the tools within Django
* middleware
* template_context_managers
* signals
* class-based views
* mixins
* templatetags

See newbie's solving problems using the wrong feature

http://stackoverflow.com/questions/550632/favorite-django-tips-features

Things to research:
- virtualenv
- iterators, generators
- unittest, nose (pyhamcrest, pyzen, twill, lettuce)
- itertools, collections

Gotchas:
- mutable arguments
- circular reference problems
- ORM lets you write dreadful queries - leaky abstraction
- Circular references -> git bisect, don't trust the error messages
  - Works fine locally but not on apache/wsgi machine
integer division
tuples need a comma
class variables
missing an __init__
casting to int

http://stackoverflow.com/questions/101268/hidden-features-of-python

Recruitment different:
- less applications
- ask for more money
- quite in demand now
- more in fashion

Teams and migration:
- Buy the books
- Sharing knowledge: sitting together, code review (github), pairing
  * set up a mailing list, wiki
- Send people to conferences
- Everyone wants to work on PHP


Cool things:
* if you're new to python, here's a few things to whet your appetite
- python -m
  python -m SimpleHTTPServer
  python -m smtpd -n -c DebuggingServer localhost:1025
  curl -s "http://feeds.delicious.com/v2/json?count=5" | python -m json.tool | less -R

https://code.djangoproject.com/wiki/NewbieMistakes

cryptic error messages

- use python in vim
  select code in visual mode and run :%! python
