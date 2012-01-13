===============================================
Introducing unittest-xml: testing XML in Python
===============================================
--------------------------------------------------------------
A simple module for making XPath assertions :: python, testing
--------------------------------------------------------------

For some reason, I keep finding myself writing unit tests that need to make
assertions about an XML document.  To avoid duplication, I've package up my
custom assertion methods as a PyPi module: ``unittest-xml``.

Sample Usage
------------

Enable the additional assert methods using a mixin:

.. sourcecode:: python

    import unittest
    from xmltest import XMLAssertions


    class SampleTestCase(unittest.TestCase, XMLAssertions):
        ...

Now suppose that the expected XML from some SUT [#]_ is:

.. sourcecode:: xml

    <?xml version="1.0" encoding="UTF-8" ?>
    <Response>
        <CardTxn>
            <authcode>060642</authcode>
            <card_scheme>Switch</card_scheme>
            <issuer country="UK">HSBC</issuer>
        </CardTxn>
        <reference>3000000088888888</reference>
        <merchantreference>1000001</merchantreference>
        <mode>LIVE</mode>
        <reason>ACCEPTED</reason>
        <status>1</status>
        <time>1071567305</time>
    </Response>

then you can make assertions about the document using 3 additional
assertions methods.

.. sourcecode:: python

        self.assertXPathNodeCount(RESPONSE, 1, 'CardTxn/authcode')
        self.assertXPathNodeText(RESPONSE, 'LIVE', 'mode')
        self.assertXPathNodeAttributes(RESPONSE, {'country': 'UK'}, 'CardTxn/issuer')

The first argument to each method is the XML string, the second is the expected value, while
the third is the XPath query.

Installation
------------

The standard way:

.. sourcecode:: bash

    pip install unittest-xml

Discussion
----------

Note, the implementation uses `ElementTree`_ and so only `a subset of the XPath specification`_
is implemented.

.. _`ElementTree`: http://docs.python.org/library/xml.etree.elementtree.html
.. _`a subset of the XPath specification`: http://effbot.org/zone/element-xpath.htm

The `code is on Github`_, as usual.

.. _`code is on Github`: https://github.com/codeinthehole/unittest-xml

.. [#] System under test
