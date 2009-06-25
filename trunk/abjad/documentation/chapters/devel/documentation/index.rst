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


Building the docs
-----------------

Abjad uses `Sphinx <http://sphinx.pocoo.org/>`_ for documentation. From the Sphinx project site:

   Sphinx is a tool that makes it easy to create intelligent 
   and beautiful documentation, written by Georg Brandl and 
   licensed under the BSD license.

To build HTML or PDF versions of the Abjad docs you will first
need to download and install Sphinx.


.. todo:: Remove old docs and rename ``documentation/doc_sphinx`` 
   to ``documentation``.
   
.. rubric:: Footnotes

.. [#] Restructured text is abbreviated :abbr:`reST` or :abbr:`ReST`
   and should not be confused with the :abbr:`REST` and :abbr:`SOAP`
   protocols in use in other development projects on the Web.
