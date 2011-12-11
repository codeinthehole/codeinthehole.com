=========================
Writing a Thesis in LaTeX
=========================

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
  includefoot option from the geometry package and set the bottom margin to
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

* thesis_without_pdfcode.tex
* thesis_with_pdfcode.tex

The appearance of both these files on the printed page will be identical;
however after compilation into PDF (see the section below) and opening in Adobe
Acrobat (or a similar PDF reader), the advantages that come with the PDF format
will be apparent.

* thesis_without_pdfcode.pdf
* thesis_with_pdfcode.pdf

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
1.4in. headheight=13.6pt is included due to to ensure compatibility with the
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

Aside from ``mathpazo``, there are several other fonts available, such as chancery,
palatino and times (all loaded in the same way).

Preamble: fancy headers (optional)
----------------------------------

Feeling a little devil-may-care? If so, you'll probably want to install some
elegant headers along each page. This is easily acheived through the fancyhdr
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
