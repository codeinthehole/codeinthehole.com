==========================
Return false with prudence
==========================
----------------------------------------------------
Returning false to indicate an error is wrong :: php
----------------------------------------------------

From "Javascript: the good parts":

    It is rarely possible for standards comittees to remove imperfections from
    a language because doing so would cause the breakdage of all of the bad
    programs that depend on those bad parts. They are usually powerless to do
    anything except heap more features on top of the existing pile of
    imperfections. 

Douglas Crockford's terse yet lucid javascript primer makes some excellent
points on writing in a language with more than its fair of share of
shortcomings. The advice is manyfold: constituting functionality or design
decisions to avoid (the "bad" and "awful" parts) as well as patterns and
practices making use of the strongest parts of the language. Essentially, one
is guided to programming within a subset of the language, avoiding the poor
quality and outright dangerous components. This chimes in well with the
notation of "programming *into* a language" rather than within in it - stressed
by the seminal "Code Complete" by Steve McConnell.

    Don't limit your programming thinking only to the concepts that are
    supported automatically by your language. The best programmers think of
    what they want to do, and then they assess how to accomplish their
    objectives with the programming tools at their disposal. 

Both these concepts are relevant to programmers of PHP - a language carrying
just as much baggage as javascript. In my experience, developers who have only
known PHP are prone to employing of a variety of bad practices and
anti-patterns. Such things are fostered by several influences, including the
forgiving nature of the language, the veritable wealth of bad advice within the
comments on the PHP manual, and a general lack of understanding of the art of
object-oriented programming. Indeed, I think it's essential that PHP developers
learn to program (and hence *think*) in other languages: python and java in
particular. Reading the work of Martin Fowler is a good place to start but
that's a topic for another time.

.. image:: /static/images/screenshots/php-manual-returning-false.jpg

One irritating programming idiom -- especially common to PHP programmers -- is
to use a return value of ``FALSE`` to indicate that something has gone wrong, or
that no valid return value could be found. Unless the only other possible
return value is ``TRUE``, this is almost always wrong.

Of course, many programmers pick up this nasty habit from the PHP standard
library itself, which employs this practice frequently. Further, it is similar
to the C and UNIX convention of returning non-zero values as error codes (and
sometimes vice-versa). The language writers of PHP have the excuse that this
was the only mechanism available back in the dark days of PHP before version 5,
before the introduction of exceptions - programmers coding today do not have
that excuse. Indeed, employing this technique betrays a lack of understanding
of what it means to program into a language rather than within it.

Instead, please consider doing one of the following:

Throw an exception
==================

When an error has occurred, a thrown exception is a clean and intent-revealing
means of handing control over to a component of your program that can deal with
the error. This saves cluttering up the normal execution path with checks for
error codes and generally leads to concise and readable code. This leads to
shorter, cleaner methods and allows the use of fluent interfaces - safe in the
knowledge that a valid object will always be returned.

So use:

.. sourcecode:: php

    try {
        // Place an order
        $orderNumber = $this->generateNewOrderNumber();
        $this->saveDeliveryAddress()
            ->saveBillingAddress()
            ->saveBatches()
            ->saveOrder($orderNumber);
    } catch (OrderCreationException $e) {
        // Rollback transaction, return friendly error message
    } 

instead of

.. sourcecode:: php

    $orderNumber = $this->generateNewOrderNumber();
    if (!$orderNumber) return false;
    $deliveryAddressSavedOk = $this->saveDeliveryAddress();
    if (!$deliveryAddressSavedOk) return false;
    $billingAddressSavedOk = $this->saveDeliveryAddress();
    if (!$billingAddressSavedOk) return false;
    ...

Using exceptions to indicate errors obeys the Command-query separation
principle, where (broadly speaking) only "getter" methods should return a value
(using fluent interfaces is a mild but acceptable violation of this
separation).  

Return ``null``, Null object or an empty collection
===================================================

Many objects will emply "finder" or factory methods responsible for looking up
and then constructing an object:

.. sourcecode:: php

    $book = Book::findByIsbn($isbn);

In this case, when no book is found, FALSE is not the appropriate return value
- either return NULL (to indicate the absence of a valid book), or employ the
Null Object pattern and return an null book object. It just feels so wrong
returning multiple types from a function. Alarm bells should ring as soon as
you see the pipe:

.. sourcecode:: php

    /**
    * @param string $isbn
    * @return Book|false
    */

A neat idiom for finder methods is to always return a iterable collection of
objects, which is simply empty when no object is found:

.. sourcecode:: php

    class Book
    {
        ...
        public static function findByIsbn($isbn)
        {
            $books =  new BookCollection; // An iterable collection object
            ...
            // Loop through database result set and add books to BookCollection
            ...
            return $books;
        }
    }

Client code can then simply iterate over the returned value - it doesn't have
to check for the presence of an item. JQuery employs this pattern extensively
with its ``$`` CSS selector and it works wonderfully. The only downside for this
is mental discomfort involved in selecting an element where there can only ever
be one: such as an element with a unique id (``$('#my_element')``).

Ultimately, there's only really one place where returning false is appropriate:
that's in a method that only returns boolean values.
