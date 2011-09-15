public: yes
tags: [jinja, python, django]
summary: |
  Why Jinja2's template engine design makes it harder for your to shoot
  yourself into the foot compared to Django's limited templating system.

Not So Stupid Template Languages
================================

Daniel Greenfeld `recently criticized
<http://pydanny.blogspot.com/2010/12/stupid-template-languages.html>`_
templating languages such as Mako, Genshi, Jinja2 or others for being more
than a stupid template language.  That of course might be valid criticism,
but there seems to be some major misunderstanding out there about what
Jinja2 compared to Django's templating system actually is.

As said by Daniel:

    I often work on projects crafted by others, some who decided for
    arcane/brilliant/idiotic reasons to mix the kernel of their
    applications in template function/macros. This is only possible in
    Smart Template Languages! If they were using a Stupid Template
    Language they would have been forced put their kernel code in a Python
    file where it applies, not in a template that was supposed to just
    render HTML or XML or plain text.

I suppose the macro part there is written especially with Jinja2 in mind
there because I know very few templating systems calling things “macros”.
In fact, the only reason Jinja2 calls its functions “macros” is that
“enddef” sounded stupid as a keyword and “endfunction” was past the
threshold of keyword lengths I was happy with.
