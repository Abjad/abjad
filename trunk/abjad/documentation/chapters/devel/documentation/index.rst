Documentation
=============

The Abjad documentation is included in its entirety when you check out
the Abjad codebase. You may add to and edit the docs as soon as you 
download and install Abjad. However, to build HTML or PDF versions of the
docs and see the results of your changes you will first need to download
and install `Sphinx <http://sphinx.pocoo.org/>`_, the automated documentation
build and management system used by Abjad and a `number of other Python
projects <http://sphinx.pocoo.org/examples.html>`_, including www.python.org.

This remaining sections of this chapter describe how to find and edit the
Abjad docs, and how to build the the docs with Sphinx.


How the docs are laid out
-------------------------

The Abjad documentation source files are included in the ``documentation``
directory of every Abjad download. ::

   abjad$ ls -d d*

   debug         directives    dots
   demos         documentation dynamics

The ``documentation`` directory contains everything 
required to build HTML, LaTeX and PDF versions of the Abjad docs,
including the page that you're reading now.
List the contents of the ``documentation`` directory and take a look around. ::

   abjad$ ls documentation

   Makefile   _templates chapters   index.rst  scr
   _static    _themes    conf.py    make.bat

The core content of the Abjad docs lives in ``documentation/chapters``. ::

   abjad$ ls documentation/chapters/

   api          background   fundamentals tutorial
   appendices   developers   introduction 

The ``documentation/chapters`` subdirectories mirror
the main sections on the front page of the Abjad docs.

What you'll find as you inspect the chapters directories, or as you 
consider adding a new chapter directory, are a collection of ``.rst`` 
files organized into directories. The ``.rst`` extension identifies files
written in restructured text, or reST, described more fully below. [#]_ ::

   abjad$ ls documentation/chapters/appendices/glossary

   index.rst


Running ``make clean``
----------------------

After you have downloaded and installed Sphinx, change to the Abjad
``documentation`` directory and use the Sphinx makefile to remove
any existing ``documentation/_build`` directory prior to making
a new build of the docs. :: 

   abjad$ cd documentation
   documentation$ make clean

   rm -rf _build/*

This removes the ``documentation/_build`` directory and its contents.
After ``make clean`` feel free to build new HTML or other versions of 
of the docs as described in the following sections.


Building the HTML docs
----------------------

Change to the Abjad ``documentation`` directory and run ``make html``. ::

   abjad$ cd documentation
   documentation$ make html

   Making output directory...
   Running Sphinx v0.6.1
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
   writing output... [100%] index                  /indexdexexexng/indexxdexindex
   writing additional files... genindex modindex search
   copying images... done
   copying static files... done
   dumping search index... done
   dumping object inventory... done
   build succeeded.

   Build finished. The HTML pages are in _build/html.

You will then find the complete HTML version of the docs
in ``documentation/_build/html``. ::

   documentation$ ls _build/
   doctress html

The output from Sphinx is verbose the first time you build the docs.
On sequent builds, Sphinx reports changes only. ::

   documentation$ make html

   sphinx-build -b html -d _build/doctrees   . _build/html
   Running Sphinx v0.6.1
   loading pickled environment... done
   building [html]: targets for 1 source files that are out of date
   updating environment: 0 added, 1 changed, 0 removed
   reading sources... [100%] chapters/devel/documentation/index
   looking for now-outdated files... none found
   pickling environment... done
   checking consistency... done
   preparing documents... done
   writing output... [100%] index                  ation/index
   writing additional files... genindex modindex search
   copying static files... done
   dumping search index... done
   dumping object inventory... done
   build succeeded.

   Build finished. The HTML pages are in _build/html.


Building a coverage report
--------------------------

Change to the Abjad ``documentation`` directory and call ``sphinx-build``
explicitly with the coverage builder, source directory and target directory. ::

   documentation$ sphinx-build -b coverage . _build/coverage
   Making output directory...
   Running Sphinx v0.6.1
   loading pickled environment... not found
   building [coverage]: coverage overview
   updating environment: 568 added, 0 changed, 0 removed
   reading sources... [ 37%] chapters/api/tools/clonewp/by_leaf_counts_with_parenta
   reading sources... [ 38%] chapters/api/tools/clonewp/by_leaf_range_with_parentag
   reading sources... [ 38%] chapters/api/tools/componenttools/get_duration_crosser

   ... (many lines omitted) ...

   reading sources... [ 85%] chapters/api/tools/spannertools/withdraw_from_containe
   reading sources... [ 95%] chapters/fundamentals/duration/interfaces_compared/ind
   reading sources... [100%] index                 t/indexdexexexng/indexxdexindex
   looking for now-outdated files... none found
   pickling environment... done
   checking consistency... done
   build succeeded.

The coverage report is now available in the ``documentation/_build/coverage``
directory. ::

   documentation$ ls _build/
   coverage doctrees html


Building other versions of the docs
-----------------------------------

Examine the Sphinx makefile in the Abjad ``documentation/`` directory
or change to the ``documentation/`` directory and type ``make`` with
no arguments to see a list of the other versions of the Abjad docs
that are available to build. ::

   documentation$ make 

   Please use `make <target>' where <target> is one of
     html      to make standalone HTML files
     dirhtml   to make HTML files named index.html in directories
     pickle    to make pickle files
     json      to make JSON files
     htmlhelp  to make HTML files and a HTML help project
     qthelp    to make HTML files and a qthelp project
     latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter
     changes   to make an overview of all changed/added/deprecated items
     linkcheck to check all external links for integrity
     doctest   to run all doctests embedded in the documentation (if enabled)


.. rubric:: Footnotes

.. [#] Restructured text is abbreviated :abbr:`reST` or :abbr:`ReST`
   and should not be confused with the :abbr:`REST` and :abbr:`SOAP`
   protocols in use in other development projects on the Web.
