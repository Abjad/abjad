Documentation
=============

The reST-based sources for the Abjad documentation are included in their
entirety in every installation of Abjad. You may add to and edit these
reST-based sources as soon as you install Abjad.  However, to build
human-readable HTML or PDF versions of the docs you will first need to download
and install Sphinx.

The remaining sections of this chapter describe how the Abjad docs are laid out
and how to build the docs with Sphinx.


How the Abjad docs are laid out
-------------------------------

The source files for the Abjad docs are included in the ``docs`` directory of
every Abjad install.  The ``docs`` directory contains everything required to
build HTML, PDF and other versions of the Abjad docs:

..  shell::

    ls -x -F docs/

The documentation sourcefiles are collected in section directories resident in
``docs/source/``:

..  shell::

    ls -x -F docs/source/

The nine section directories in ``docs/source`` mirror the frontpage sections
of the Abjad documentation. There are section directories for the start here,
system overview, examples, tutorials, reference manual, developer
documentation, appendices, and api and "in conversation" sections of
documentation.

When you look inside a section directory you'll find a collection of chaper
directories.

Here are the reference manual chapter directories:

..  shell::

    ls -x -F docs/source/reference_manual

And when you look inside a chapter directory you'll find an ``.rst.raw`` file,
and ``.rst`` file and an ``images/`` directory:

..  shell::

    ls -x -F docs/source/reference_manual/notes


Installing Sphinx
-----------------

Sphinx is the automated documentation system used by Python, Abjad and `other
projects <http://sphinx.pocoo.org/examples.html>`_ implemented in Python.
Because Sphinx is not included in the Python standard library you will probably
need to download and install it.

First check to see if Sphinx is already installed on your machine:

..  shell::

    sphinx-build --version

If Sphinx responds then the program is already installed on your machine.
Otherwise visit the `Sphinx <http://sphinx.pocoo.org/>`_ website.


Using ``ajv api``
-----------------

The ``ajv`` application ships with Abjad. The application helps developers
manage the Ajbad codebase. The ``ajv`` subcommand ``api`` allows for building
and cleaning various formats of Sphinx documentation.

..  shell::

    ajv api --help

Removing old builds of the documentation
----------------------------------------

To remove old builds of the documentation, use the ``clean`` command:

..  code-block:: bash

    abjad$ ajv api --clean

Building the HTML docs
----------------------

You can use ``ajv`` to build the HTML docs. It doesn't matter what directory
you're in when you run the following command:

..  code-block:: bash

    abjad$ ajv api -M
    Now writing ReStructured Text files ...

    ... done.

    Now building the HTML docs ...

    sphinx-build -b html -d build/doctrees   source build/html
    Making output directory...
    Running Sphinx v1.1.3
    loading pickled environment... not yet created
    loading intersphinx inventory from http://docs.python.org/2.7/objects.inv...
    building [html]: targets for 1131 source files that are out of date
    updating environment: 1131 added, 0 changed, 0 removed
    reading sources... [  1%] api/demos/part/PartCantusScoreTemplate/PartCantusScore
    reading sources... [  4%] api/tools/abjadbooktools/AbjadBookProcessor/AbjadBookP
    reading sources... [  4%] api/tools/abjadbooktools/AbjadBookScript/AbjadBookScri
    reading sources... [  4%] api/tools/abjadbooktools/HTMLOutputFormat/HTMLOutputFo
    reading sources... [  4%] api/tools/abjadbooktools/LaTeXOutputFormat/LaTeXOutput
    reading sources... [  4%] api/tools/abjadbooktools/ReSTOutputFormat/ReSTOutputFo
    reading sources... [  5%] api/tools/scoretools/Chord/Chord                      
    ...
    ...
    ...
    copying images... [ 89%] reference_manual/lilypond_commands/images/index-2.
    copying images... [ 93%] tutorials/understanding_time_signatures/images/ind
    copying images... [ 94%] tutorials/working_with_threads/images/thread-resolution
    copying images... [100%] reference_manual/staves/images/index-8.png             
    copying static files... done
    dumping search index... done
    dumping object inventory... done
    build succeeded.

    Build finished. The HTML pages are in build/html.

You will then find the complete HTML version of the docs in the
``docs/build/html/`` directory: 

..  shell::

    ls docs/build/

The output from Sphinx is verbose the first time you build the docs.  On
sequent builds, Sphinx reports changes only:

..  code-block:: bash

    abjad$ ajv api -M
    Now writing ReStructured Text files ...

    ... done.

    Now building the HTML docs ...

    sphinx-build -b html -d build/doctrees   source build/html
    Running Sphinx v1.1.3
    loading pickled environment... done
    building [html]: targets for 0 source files that are out of date
    updating environment: 0 added, 0 changed, 0 removed
    looking for now-outdated files... none found
    no targets are out of date.

    Build finished. The HTML pages are in build/html.


Building a PDF of the docs
--------------------------

Building a PDF of the docs is almost as simple as building the HTML
documentation:

..  code-block:: bash

    abjad$ ajv api -M --format latexpdf
    Now writing ReStructured Text files ...

    ... done.

    Now building the LATEXPDF docs ...

    sphinx-build -b latex -d build/doctrees   source build/latex
    Running Sphinx v1.2b1
    loading pickled environment... done
    building [latex]: all documents
    updating environment: 0 added, 1 changed, 0 removed
    reading sources... [100%] developer_documentation/index                                                                                                                             
    looking for now-outdated files... 10 found
    pickling environment... done
    checking consistency... done
    processing Abjad.tex..
    ...
    ...
    ...
    Transcript written on AbjadAPI.log.
    pdflatex finished; the PDF files are in build/latex.

The resulting docs will appear as ``Abjad.pdf`` and ``AbjadAPI.pdf`` in the
LaTeX build directory, ``docs/build/latex``.


Building a coverage report
--------------------------

Build the coverage report with ``ajv api`` and the ``coverage`` format.

..  code-block:: bash

    abjad$ ajv api -M --format coverage
    Now writing ReStructured Text files ...

    ... done.

    Now building the COVERAGE docs ...

    Running Sphinx v1.2b1
    loading pickled environment... done
    building [coverage]: coverage overview
    updating environment: 0 added, 1 changed, 0 removed
    reading sources... [100%] api/tools/commandlinetools/BuildAPIScript/BuildAPIScript                                                                                              
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    build succeeded.

The coverage report is now available in the ``docs/build/coverage`` directory:

..  code-block:: bash

    docs$ ls build/
    coverage doctrees html


Building other versions of the docs
-----------------------------------

Examine the Sphinx makefile in the Abjad ``docs/`` directory or change to the
``docs/`` directory and type ``make`` with no arguments to see a list of the
other versions of the Abjad docs that are available to build:

..  code-block:: bash

    docs$ make

    Please use "make <target>" where <target> is one of
    html       to make standalone HTML files
    dirhtml    to make HTML files named index.html in directories
    singlehtml to make a single large HTML file
    pickle     to make pickle files
    json       to make JSON files
    htmlhelp   to make HTML files and a HTML help project
    qthelp     to make HTML files and a qthelp project
    devhelp    to make HTML files and a Devhelp project
    epub       to make an epub
    latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter
    latexpdf   to make LaTeX files and run them through pdflatex
    text       to make text files
    man        to make manual pages
    texinfo    to make Texinfo files
    info       to make Texinfo files and run them through makeinfo
    gettext    to make PO message catalogs
    changes    to make an overview of all changed/added/deprecated items
    linkcheck  to check all external links for integrity
    doctest    to run all doctests embedded in the documentation (if enabled)
    book       to run abjad-book on all ReST files in source


Updating Sphinx
---------------

It is important periodically to update your version of Sphinx.  If you used
``pip`` to install Sphinx then the usual command to update Sphinx is
this:

..  code-block:: bash

    abjad$ sudo pip install --upgrade Sphinx
