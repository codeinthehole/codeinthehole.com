=========================
Writing a Thesis in LaTeX
=========================
-----------------------------------------------------
A short guide to getting things to look nice :: latex
-----------------------------------------------------

Overview
========

This article is a guide to constructing a decent parent file for a thesis or
dissertation compiled in Latex. The specific details implemented here, and
included in the example files, are those set out by the guidelines for
submission to the University of Nottingham, but can be easily amended to suit
any sensible requirements.

Considerable attention has been paid to presenting the final document as a PDF
file, which keeps the file size managable (compared to postscript) and allows
groovy addons such as hyperlinks and back-referencing. However, several hacks
are required to attain good functionality from your PDF file and these can give
the latex code a mysterious (and messy) appearance in places. While I highly
recommend the inclusion of the PDF-related commands, they are not strictly
necessary and can be ignored - especially if you are new to Latex. 

.. warning:: I wrote this article after finishing my PhD in 2005.  I haven't
    done any Latex since and am thus very rusty.  Ultimately, these
    days I'm unlikely to be able to answer many questions on this topic. Sorry about
    that.

Note for Windows users
======================

The code outlined below was designed and implemented on the unix system at
Nottingham. For those of you unfortunate enough to be running a Windows box, a
number of problems may arise when using the below code:

* First off, not all the packages used will be present and will need to be
  installed. Probably the easiest way to do this is to google the package name
  with the extension ``.sty`` and save this file in the ``C:\VTEX\l2e\`` directory of
  your machine. Note that for the ``natbib`` package, you will also need to
  download the relevant ``.bst`` file, which in this case is ``unsrtnat.bst``.
* Also, many of the packages that are installed locally may need updating. For
  instance, the computers I have tested on both have old versions of the
  ``geometry`` and ``caption`` packages, which cause Latex to return errors. To resolve
  these problems, either download the latest versions, or remove the
  ``includefoot`` option from the ``geometry`` package and set the bottom margin to
  1.4in.

Also, the code for compiling to PDF does not work so well in Windows, and so it
is recommended that Windows users use the template without PDF code.

Requirements
============

The guidelines for theses to be submitted to the University of Nottingham specify that:

1. the document should be presented on single-sided a4 paper and typeset in a
   double-spaced size 10-12 font;
2. the left-hand margin should be at least 1.5 inches (4cm) to allow for
   binding;
3. the other three margins should be at least 1 inch (2.5cm).

Other settings such as the way chapter headings are formatted, and whether
headers are included, are not specified and are up to the user. In this case,
we'll install headers and tinker with the chapter formatting.

Template files
==============

Here are the template files which this page explains:

* `thesis_without_pdfcode.tex`_
* `thesis_with_pdfcode.tex`_

.. _`thesis_without_pdfcode.tex`: /static/downloads/thesis_without_pdfcode.tex
.. _`thesis_with_pdfcode.tex`: /static/downloads/thesis_with_pdfcode.tex

The appearance of both these files on the printed page will be identical;
however after compilation into PDF (see the section below) and opening in Adobe
Acrobat (or a similar PDF reader), the advantages that come with the PDF format
will be apparent.

* `thesis_without_pdfcode.pdf`_
* `thesis_with_pdfcode.pdf`_

.. _`thesis_without_pdfcode.pdf`: /static/downloads/thesis_without_pdfcode.pdf
.. _`thesis_with_pdfcode.pdf`: /static/downloads/thesis_with_pdfcode.pdf

The rest of this page is devoted to explaining the code in these files.

Document structure
==================

The document begins in a standard and entirely self-explanatory manner.

.. sourcecode:: latex

    \documentclass[11pt,a4paper]{report}

Preamble: essential packages
----------------------------

Next, the essential packages are loaded:

.. sourcecode:: tex

    \usepackage{amsmath, amssymb, amsthm} % AMS packages
    \usepackage{graphicx,color}           % Packages for graphics and color
    \usepackage[left=1.5in, right=1in, top=1in, bottom=1in, includefoot, headheight=13.6pt]{geometry}
    \usepackge[T1]{fontenc}               % Ensure correct font encoding

where the ``geometry`` package has been loaded to allow the margins to be set in a
neat and consistent way. The non-obvious option ``includefoot`` ensures that the
footer (which only contains the pagenumber) is included in the page and is thus
1 inch above the bottom of the page. Note that this option is only available in
recent versions of the package: if you're using an old version and can't/won't
upgrade, then remove the offending option and extend the bottom margin to
1.4in. ``headheight=13.6pt`` is included due to to ensure compatibility with the
``fancyhdr`` package (and is not required if you don't use the ``fancyhdr`` package).
Also quite essential is the ``natbib`` package:

.. sourcecode:: latex

    \includepackage[square, comma, numbers, sort&compress]{natbib}

where the various options ensure that references appear in the document as:

    ...boiled dog can do maths claims experimenter [10,12,15-18].
    
Alternative referencing styles are easily implemented, see the natbib help file
for more details. In fact, to use the ``natbib`` package, you'll have to read
at least a few lines of the help file so you understand the difference between
``\citet`` and ``\citep``, and I insist you do that now.

Preamble: custom captions (optional)
------------------------------------

We now set the figure captions to be elegant and dignified:

.. sourcecode:: latex

    \usepackage[hang, small, bf, margin=20pt, tableposition=top]{caption}
    \setlength{\abovecaptionskip}{0pt}

Note that early versions of this package don't support the ``margin=`` and
``tableposition=`` options; in this case, these trimmings will have to be ignored.

Preamble: custom fonts (optional)
---------------------------------

You can also choose an alternative font for both the text and the mathematical
characters. This can be acheived by:

.. sourcecode:: latex

    \usepackage{mathpazo}

Aside from ``mathpazo``, there are several other fonts available, such as ``chancery``,
``palatino`` and ``times`` (all loaded in the same way).

Preamble: fancy headers (optional)
----------------------------------

Feeling a little devil-may-care? If so, you'll probably want to install some
elegant headers along each page. This is easily acheived through the ``fancyhdr``
package:

.. sourcecode:: latex

    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \rhead{}
    \lhead{\nouppercase{\textsc{\leftmark}}}
    \renewcommand{\headrulewidth}{0pt}
    \makeatletter
    \renewcommand{\chaptermark}[1]{\markboth{\textsc{\@chapapp}\ \thechapter:\ #1}{}}
    \makeatother

The final complicated-looking three lines simply ensure that the headings for
appendices are formatted correctly. (Without these lines, what should read
"Appendix A" is set as "Chapter A".)

Preamble: customised chapter/section headings (optional)
--------------------------------------------------------

We now make use of several customisation options that are bundled with the sectsty package.

.. sourcecode:: latex

    \usepackage{sectsty}
    \chapterfont{\large\sc\centering}
    \chaptertitlefont{\centering}
    \subsubsectionfont{\centering}

These alter the appearance of the first page of each chapter to have a centred
title, with the word "chapter" set in small capitals immediately above. Feel
free to employ your own individual and highly refined tastes here in choosing
your own chapter/section settings.  

Preamble: pdf options (optional)
--------------------------------

If you want to publish your thesis on the internet, or even just to email it to
someone, then you'll want to store it in the ubiquitous PDF format. Doing so
offers some neat facilities, such as hyperlinking, which are implemented by the
``hyperref`` package:

.. sourcecode:: latex

    \usepackage[ps2pdf=true,colorlinks]{hyperref}
    \usepackage[figure,table]{hypcap} % Correct a problem with hyperref
    \hypersetup{
        bookmarksnumbered,
        pdfstartview={FitH},
        citecolor={black},
        linkcolor={black},
        urlcolor={black},
        pdfpagemode={UseOutlines}
    }

There are various other options you can pass to your favourite PDF reader via
the ``\hypersetup`` command, such as ``pdftitle``, ``pdfauthor`` and ``pdfsubject``; however,
they're not really essential. Note that the hyperlink colours have all been set
to black for consistent printing. Should you want to distribute your thesis
over the web, then it would be advisable to set these colours to red or
something similarly vibrant and exciting.

Things get a little messy now as a hack is required to ensure the hyperlinks actually jump to the right place.

.. sourcecode:: latex

    \makeatletter
    \newcommand\org@hypertarget{}
    \let\org@hypertarget\hypertarget
    \renewcommand\hypertarget[2]{%
    \Hy@raisedlink{\org@hypertarget{#1}{}}#2%
    } \makeatother

No need to worry about this code, let's just move straight on.

Preamble: page layout
---------------------

We now set various parameters to alter the general page layout:

.. sourcecode:: latex

    \parindent 0pt
    \parskip 1ex
    \renewcommand{\baselinestretch}{1.33}

The first two of these commands alter the paragraph formatting so that new
paragraphs are not indented but separated from the previous one by a small
amount of whitespace; the third sets the line spacing. The sharp-eyed among you
will notice the discrepancy between our chosen line-spacing and that dictated
by the university guidelines. However, no matter how poor your eyesight is,
you'll quickly appreciate that true double line-spacing (set with
``\renewcommand(\baselinestretch}{2}``) looks rubbish. In addition, Nottingham
University are perfectly happy to accept theses set with the above
line-spacing, which is more pleasing to the eye.

Some final settings:

.. sourcecode:: latex

    \numberwithin{equation}{section}       % Tinker with equation numbering
    \renewcommand{\bibname}{References}    % Alter appearance of table of contents slightly
    \renewcommand{\contentsname}{Contents}
    \pagenumbering{roman}                  % Sets the pagenumbering to Roman nunerals to begin with
    \bibliographystyle{unsrtnat}           % Sets bibliography style file (see natbib literature)

Set which chapters to include when Latex is next run. The advantage of this
method is that all your cross-references are remembered and Latex does not spit
out loads of warnings.

.. sourcecode:: latex

    \includeonly{chapter1,chapter2,chapter3,conclusions,appendices}

Main matter
-----------

We now begin the document in earnest and define a suitable title:

.. sourcecode:: latex

    \begin{document}
    \title{
    \huge{\textbf{Collected studies in\\pseudoscience}}\\[1.2cm]
    \Large{Nathan P. Utah, MMath.} \\[1.2cm]
    \Large{Thesis submitted to The University of Nottingham \\
    for the degree of Doctor of Philosophy} \\[1cm]
    \Large{November 2005} }
    \author{} \date{}
    \pdfbookmark[0]{Titlepage}{title} % Sets a PDF bookmark for the title page
    \maketitle

followed by a dedication:

.. sourcecode:: latex

    \newpage \vspace*{8cm}
    \pdfbookmark[0]{Dedication}{dedication} % Sets a PDF bookmark for the dedication
    \begin{center}
    \large Dedicated to the steel workers of America
    \end{center}

We now construct an abstract:

.. sourcecode:: latex

    \newpage
    \pdfbookmark[0]{Abstract}{abstract} % Sets a PDF bookmark for the abstract
    \chapter*{Abstract}
    \textsc{The celebrated number} -17 was discovered in Manchester in 1989 ...

some acknowledgements:

.. sourcecode:: latex

    \pdfbookmark[0]{Acknowledgements}{acknowledgements} % Sets a PDF bookmark for the acknowledements
    \chapter*{Acknowledgements}
    I would like to thank Rambo, my pet fishfinger...

and a contents page:

.. sourcecode:: latex

    \pdfbookmark[0]{Contents}{contents} % Sets a PDF bookmark for the contents page
    \tableofcontents

Now, we alter the pagenumbering to arabic and point to the relevant chapter files:

.. sourcecode:: latex

    \newpage
    \pagenumbering{arabic}
    \include{chapter1}
    \include{chapter2}
    \include{chapter3}
    ...
    \include{conclusions}
    \include{appendices}

All your chapter files should be included here; to save time when editing, use
the ``\includeonly`` command to specify which chapters to compile.

Finally, we make sure there is a link to the references section in the table of
contents and reference the correct bibiography file (which in this case is
called ``bibliography.bib``).

.. sourcecode:: latex

    \phantomsection % Ensures that a PDF bookmark is set here
    \addcontentsline{toc}{chapter}{References}
    \bibliography{bibliography}
    \end{document}

And there we have it: a complete thesis parent file that not only looks good on
the printed page, but is fully functional and hyperlinked in PDF format.

Compiling to PDF
----------------

Whether you've included all the red PDF commands or not, you can convert your
TEX file to PDF by running (in unix):

.. sourcecode:: bash

    $ latex thesis_with_pdfcode.tex
    $ dvips thesis_with_pdfcode.dvi
    $ ps2pdf -sPAPERSIZE=a4 thesis_with_pdfcode.ps

The additional argument to ``ps2pdf`` is required as the default paper size is US
Letter. Note that you will probably need to bibtex your thesis file before
running latex for the final time.

For Windows, first open a command window by going ``Start->Run`` and entering ``cmd``. Provided
MiKTeX and GhostScript are correctly installed then the necessary commands are:

.. sourcecode:: bash

    > latex thesis_with_pdfcode.tex
    > dvips thesis_with_pdfcode.dvi
    > ps2pdf.bat -sPAPERSIZE#a4 thesis_with_pdfcode.ps thesis_with_pdfcode.pdf

The syntax for ``ps2pdf`` is slightly different in Windows compared to Unix - and
note that the output pdf filename MUST be specified, else the ps file is
overwritten and corrupted.


.. tip::
    Sponsored links: 
    Become IT expert using latest `braindump`_. Go through the `350-001 dumps`_ to
    learn what's new going to happen in industry. We offer up to date `70-680 dumps`_
    written by industry's top expert to help you excel in your field. 
    
.. _`braindump`: http://www.braindumps.com/
.. _`350-001 dumps`: http://www.braindumps.com/350-001.htm
.. _`70-680 dumps`: http://www.braindumps.com/70-680.htm
