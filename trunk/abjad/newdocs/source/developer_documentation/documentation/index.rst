Docs
====

The reST-based sources for the Abjad documentation are included in their entirety 
in every installation of Abjad. You may add to and edit these reST-based sources 
as soon as you install Abjad. 
However, to build human-readable HTML or PDF versions of the docs you will first need to download
and install Sphinx.


The remaining sections of this chapter describe how the Abjad docs are laid out
and how to build the docs with Sphinx.


How the Abjad docs are laid out
-------------------------------

The source files for the Abjad docs are included in the ``docs`` 
directory of every Abjad install.
The ``docs`` directory contains everything
required to build HTML, PDF and other versions of the Abjad docs. ::

    abjad$ ls docs/
    Makefile    _templates  chapters    index.rst  scr
    _static     _themes     conf.py     make.bat

The bulk of the Abjad docs live in ``docs/chapters``.
The chapter directories mirror the main sections on Abjad documentation.
What you'll find as you inspect the chapter directories are a 
collection of ``.rst`` files organized into groups.
The ``.rst`` extension identifies files written in restructured text.

One example::

    abjad$ ls docs/chapters/appendices/glossary
    index.rst


Installing Sphinx
-----------------

Sphinx is the automated documentation system used by Python, Abjad 
and `other projects <http://sphinx.pocoo.org/examples.html>`_
implemented in Python. Because Sphinx is not included in the Python standard library you
will probably need to download and install it.

First check to see if Sphinx is already installed on your machine. ::

    $ sphinx-build --version

If Sphinx responds then the program is already installed on your machine.
Otherwise visit the `Sphinx <http://sphinx.pocoo.org/>`_ website.


Removing old builds of the docs
-------------------------------

After installing Sphinx, change to the Abjad ``docs`` directory 
and use the Sphinx makefile to remove any existing ``docs/_build`` 
directory prior to making a new build of the docs. ::

    abjad$ cd docs

::

    docs$ make clean
    rm -rf _build/*


Generating the Abjad API
------------------------

The ``docs/scr`` directory includes a script to generate the Abjad API.  
Run this script before building the Abjad docs for the first time. ::

    docs$ scr/make-abjad-api
    Building TOC tree ...
    Now making Sphinx TOC ...

    ... Done.

    Now building the HTML docs ...

    sphinx-build -b html -d _build/doctrees   . _build/html
    Running Sphinx v1.0.7
    loading pickled environment... done

    ... (many lines omitted) ...

    Build finished. The HTML pages are in _build/html.

Rerun ``make-abjad-api`` any time you add or remove a public class, 
method or function from the codebase.


Building the HTML docs
----------------------

Change to the Abjad ``docs`` directory and run ``make html``. ::

    abjad$ cd docs

::

    docs$ make html
    sphinx-build -b html -d _build/doctrees   . _build/html
    Running Sphinx v1.0.7
    loading pickled environment... not found
    building [html]: targets for 568 source files that are out of date
    updating environment: 568 added, 0 changed, 0 removed
    reading sources... [ 13%] chapters/api/debug/debugghandlertoregatorsg
    reading sources... [ 37%] chapters/api/tools/clonewp/by_leaf_counts_with_parenta
    reading sources... [ 38%] chapters/api/tools/clonewp/by_leaf_range_with_parentag
    reading sources... [ 38%] chapters/api/tools/componenttools/get_duration_crosser
    reading sources... [ 38%] chapters/api/tools/componenttools/get_duration_preprol
    reading sources... [ 39%] chapters/api/tools/componenttools/get_le_duration_prol

    ... (many more lines omitted) ...

    writing output... [ 85%] chapters/api/tools/spannertools/give_attached_to_childr
    writing output... [ 95%] chapters/fundamentals/duration/interfaces_compared/inde
    writing output... [100%] index                        /indexdexexexng/indexxdexindex
    writing additional files... genindex modindex search
    copying images... done
    copying static files... done
    dumping search index... done
    dumping object inventory... done
    build succeeded.

    Build finished. The HTML pages are in _build/html.

You will then find the complete HTML version of the docs in ``docs/_build/html``. ::

    docs$ ls _build/
    doctrees html

The output from Sphinx is verbose the first time you build the docs.
On sequent builds, Sphinx reports changes only. ::

    docs$ make html
    sphinx-build -b html -d _build/doctrees    . _build/html
    Running Sphinx v1.0.7
    loading pickled environment... done
    building [html]: targets for 1 source files that are out of date
    updating environment: 0 added, 1 changed, 0 removed
    reading sources... [100%] chapters/devel/documentation/index
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    writing output... [100%] index                        ation/index
    writing additional files... genindex modindex search
    copying static files... done
    dumping search index... done
    dumping object inventory... done
    build succeeded.

    Build finished. The HTML pages are in _build/html.


Building a PDF of the docs
--------------------------

Building a PDF of the docs is a two-step process.
First you build a LaTeX version of the docs.
Then you typeset the LaTeX docs as a PDF.

First change to the Abjad docs directory. ::

    abjad$ docs

Then make LaTeX sources of the docs. ::

    docs$ make latex
    sphinx-build -b latex -d _build/doctrees   . _build/latex
    Running Sphinx v1.0.7
    loading pickled environment... done
    building [latex]: all documents
    updating environment: 0 added, 0 changed, 0 removed
    looking for now-outdated files... none found
    processing Abjad.tex... index chapters/start_here/abjad/index chapters/examples/bartok...

    (... many lines omitted ...)

    ...ndices/pitch_conventions/images/example-3.png chapters/examples/ligeti/images/desordre.jpg
    copying TeX support files... done
    build succeeded.

    Build finished; the LaTeX files are in _build/latex.
    Run `make all-pdf' or `make all-ps' in that directory to run these through (pdf)latex.

Now follow the instructions provided by Sphinx and change to the LaTeX build directory. ::

    docs$ cd _build/latex/

Then make a PDF version of the docs from the LaTeX sources. ::

    latex$ make all-pdf

    pdflatex  'Abjad.tex'
    This is pdfTeXk, Version 3.141592-1.40.3 (Web2C 7.5.6)
     %&-line parsing enabled.
    entering extended mode
    (./Abjad.tex
    LaTeX2e <2005/12/01>
    Babel <v3.8h> and hyphenation patterns for english, usenglishmax, dumylang, noh
    yphenation, arabic, basque, bulgarian, coptic, welsh, czech, slovak, german, ng
    erman, danish, esperanto, spanish, catalan, galician, estonian, farsi, finnish,

    (... many lines omitted ...)

The resulting docs will appear as ``Abjad.pdf`` in the LaTeX build directory
you're currently in.


Building a coverage report
--------------------------

Change to the Abjad ``docs`` directory and call ``sphinx-build``
explicitly with the coverage builder, source directory and target directory. ::

    docs$ sphinx-build -b coverage . _build/coverage
    Making output directory...
    Running Sphinx v1.0.7
    loading pickled environment... not found
    building [coverage]: coverage overview
    updating environment: 568 added, 0 changed, 0 removed
    reading sources... [ 37%] chapters/api/tools/clonewp/by_leaf_counts_with_parenta
    reading sources... [ 38%] chapters/api/tools/clonewp/by_leaf_range_with_parentag
    reading sources... [ 38%] chapters/api/tools/componenttools/get_duration_crosser

    ... (many lines omitted) ...

    reading sources... [ 85%] chapters/api/tools/spannertools/withdraw_from_containe
    reading sources... [ 95%] chapters/fundamentals/duration/interfaces_compared/ind
    reading sources... [100%] index                      t/indexdexexexng/indexxdexindex
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    build succeeded.

The coverage report is now available in the ``docs/_build/coverage``
directory. ::

    docs$ ls _build/
    coverage doctrees html


Building other versions of the docs
-----------------------------------

Examine the Sphinx makefile in the Abjad ``docs/`` directory
or change to the ``docs/`` directory and type ``make`` with
no arguments to see a list of the other versions of the Abjad docs
that are available to build. ::

    docs$ make
    Please use `make <target>' where <target> is one of
        html        to make standalone HTML files
        dirhtml   to make HTML files named index.html in directories
        pickle    to make pickle files
        json        to make JSON files
        htmlhelp  to make HTML files and a HTML help project
        qthelp    to make HTML files and a qthelp project
        latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter
        changes   to make an overview of all changed/added/deprecated items
        linkcheck to check all external links for integrity
        doctest   to run all doctests embedded in the documentation (if enabled)


Inserting images with ``abjad-book``
------------------------------------

Use :doc:`abjad-book</chapters/developer_documentation/abjad_book/index>` to insert
snippets of notation in the docs you write in reST.

Embed Abjad code between open and close \<abjad\> \</abjad\> tags in your
``.rst.raw`` sourcefile and then call ``abjad-book``
to create a pure ``.rst`` file. ::

    abjad-book foo.rst.raw foo.rst

    Parsing file ...
    Rendering "example-1.ly" ...
    Rendering "example-2.ly" ...

You will need to build the HTML docs again to see your work. ::

    make html


Updating Sphinx
---------------

It is important periodically to update your version of Sphinx.
If you used ``easy_install`` to install Sphinx then the usual command
to update Sphinx is this::

    $ sudo easy_install -U Sphinx

This will usually work. But if Sphinx fails to update then it may be because you
have multiple versions of Python installed on your computer. (This tends especially
to be the case under Apple's OS X.)

To get around this first note the version of Python you're currently running::

    $ python --version
    Python 2.6.1

Then use a version-explicit form of ``easy_install`` to update Sphinx::

    $ sudo easy_install-2.6 -U Sphinx
