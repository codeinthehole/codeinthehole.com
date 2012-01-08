================================
Testing XML in python's unittest
================================

For testing XML:

Assume that the expected XML is:

.. sourcecode:: xml

    <?xml version="1.0" encoding="UTF-8" ?>
    <Response>
        <CardTxn>
            <authcode>060642</authcode>
            <card_scheme>Switch</card_scheme>
            <country>United Kingdom</country>
            <issuer>HSBC</issuer>
        </CardTxn>
        <datacash_reference>3000000088888888</datacash_reference>
        <merchantreference>1000001</merchantreference>
        <mode>LIVE</mode>
        <reason>ACCEPTED</reason>
        <status>1</status>
        <time>1071567305</time>
    </Response>

then you can now test the values of a element using:

.. sourcecode:: python

    class ResponseTests(TestCase, XmlAssertions):

        def test_country_is_uk(self):
            self.assertXmlElementEquals(RESPONSE, 'United Kingdom',
                                        'Response.CardTxn.country')

The implementation of this mixin is simple:

.. sourcecode:: python

    class XmlAssertions(object):

        def assertXmlElementEquals(self, xml_str, value, element_path):
            doc = parseString(xml_str)
            elements = element_path.split('.')
            parent = doc
            for element_name in elements:
                sub_elements = parent.getElementsByTagName(element_name)
                if len(sub_elements) == 0:
                    self.fail("No element matching '%s' found using XML string '%s'" % (element_name, element_path))
                    return
                parent = sub_elements[0]
            self.assertEqual(value, parent.firstChild.data)

