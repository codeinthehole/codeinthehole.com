=====================================
Auto-generating an FAQ with Prototype
=====================================
---------------------------------------------
A lazy way of generating an FAQ :: javascript
---------------------------------------------

Have just been writing an FAQ page for commandlinefu.com. Documenting is always
tiresome, but FAQs particularly so when hand-coding the HTML links between each
question and the summary table at the top of the page.

Javascript to the rescue: I cobbled together a quick Prototype script which
automatically generates the FAQ summary links by parsing the DOM for the
appropriate links:

.. sourcecode:: javascript

    document.observe('dom:loaded', function(){
        $$('a.question').each(function(ele){
            var id = ele.innerHTML.unescapeHTML().gsub(/[^\w- ]/, '').gsub(/[\s-]+/, '-').toLowerCase();
            ele.writeAttribute({id: id});
            var link = new Element('a', {href: '#'+id})
                .update(ele.innerHTML)
                .observe('click', function(event){
                    event.stop();
                    Effect.ScrollTo(ele); 
                });
            $('questions').insert(new Element('li').insert(link));
        });
    });
    
Now, all I have to do is write my FAQ ensuring the questions live in anchor
tags with the class "question" and there is an empty list tag at the top of the
page to house the summary block.

Here's two snapshots the relevant section of the DOM before and after the
dom:loaded event has fired. Before:

.. sourcecode:: javascript

    <ul id="questions"></ul>
    <dl>
        <dt><a class="question">What is this site?</a></dt>
        <dd>...</dd>
        <dt><a class="question">Who created this site?</a></dt>
        <dd>...</dd>
    </dl>

and after:

.. sourcecode:: javascript

    <ul id="questions">
        <li><a href="#what-is-this-site">What is this site?</a></li>
        <li><a href="#who-created-this-site">Who created this site?</a></li>
    </ul>
    <dl>
        <dt><a class="question" id="what-is-this-site">What is this site?</a></dt>
        <dd>...</dd>
        <dt><a class="question" id="who-created-this-site">Who created this site?</a></dt>
        <dd>...</dd>
    </dl>

As you can see, the javascript simply extracts the relevant content from the
questions and inserts the appropriate identities and links into the DOM to form
the quick-links. Using the ``Effect.ScrollTo`` function also gives a pleasant user
experience.
