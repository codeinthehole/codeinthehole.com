======================================
Ingenious use of an anonymous function
======================================
--------------------------------------
An element Lambda employment :: python
--------------------------------------

Just stumbled across a gem of a question whilst idly browsing `Stack Overflow`_:

.. _`Stack Overflow`: http://stackoverflow.com/

    Design a function ``f``, such that: ``f(f(n)) == -n`` where ``n`` is a 32-bit signed
    integer; you can't use complex numbers arithmetic.

Interesting in its own right, what makes this particularly intriguing is that
the question doesn't specify a language to use - indeed, the choice of language
has a major say in the range of solutions available. The following solution in
Python is stunningly elegant:

.. sourcecode:: python

    def f(x):
        if isinstance(x, int):
            return (lambda: -x)
        else:
            return x()

The use of a lambda function is very clever but does feel like cheating a
little. Nevertheless, such a solution was a sharp reminder of the dangers of
being too versed in a particular language (PHP in my case) such that it's hard
to think outside the language constraints. Of course, the above solution can be
implemented in any language that supports anonymous functions.

The less clever but more "natural" solution (at least to a mathematician) is
for ``f`` to toggle the parity of ``n``, multiplying by -1 only for one parity (the
cases of positive and negative n need handling separately). It's fairly easy to
build up the solution by considering in sequence ``n=0,1,2,3,...`` - see the
following clunky PHP implementation:

.. sourcecode:: python

    function f($n)
    {
        if (0 == $n) return 0;
        if ($n > 0) {
            return ($n % 2 == 1) ? $n + 1 : 1 - $n;
        } else {
            return ($n % 2 == 1) ? $n - 1 : -($n + 1);
        }
    }

