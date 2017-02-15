=================================
Creating large XML files with PHP
=================================
------------------------------------------------------------
Using PHP's ``DomDocument`` to create large XML files :: PHP
------------------------------------------------------------

When creating large XML files with PHP, there are some important considerations
to bear in mind with regards to scalability. There are several libraries
available for writing XML files of small to intermediate size (such as
DOMDocument), but when dealing with very large files (eg. > 500Mb, or several
million elements), these libraries are no longer useful as the size of the file
then can create is memory-bound.

For example, DOMDocument stores the XML tree in memory while it is being built
- you then flush it out to file after all elements have been created:

.. sourcecode:: php

    <?php
    $dom = new DOMDocument('1.0');
    for ($i=0; $i<=10000; ++$i) {
        $root = $dom->createElement('message');
        $dom->appendChild($root);
        $content = $dom->createElement('content');
        $root->appendChild($content)
        $content->appendChild($dom->createTextNode('Example content'));
    }
    // Flush XML from memory to file in one go
    file_put_contents('example.xml', $dom->saveXML());

However, this doesn't scale once your feed size starts exceeding the available
memory (tweaking memory settings in php.ini is only a short-term fix). A good
solution to this is to use the XMLWriter library as this provides the ability
to periodically flush the XML in memory out to file. By doing so, you reclaim
the memory so you can keep building the XML tree without exceeding memory
limitations.

.. sourcecode:: php

    <?php
    $xmlWriter = new XMLWriter();
    $xmlWriter->openMemory();
    $xmlWriter->startDocument('1.0', 'UTF-8');
    for ($i=0; $i<=10000000; ++$i) {
        $xmlWriter->startElement('message');
        $xmlWriter->writeElement('content', 'Example content');
        $xmlWriter->endElement();
        // Flush XML in memory to file every 1000 iterations
        if (0 == $i%1000) {
            file_put_contents('example.xml', $xmlWriter->flush(true), FILE_APPEND);
        }
    }
    // Final flush to make sure we haven't missed anything
    file_put_contents('example.xml', $xmlWriter->flush(true), FILE_APPEND);

Here we flush the XML in memory to file every 1000 iterations. This ensures
that memory usage is capped and opens up the possiblity of creating very large
XML files.
