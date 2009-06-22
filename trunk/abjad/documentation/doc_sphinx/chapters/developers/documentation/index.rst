Writing documentation
=====================

The Abjad documentation is included in its entirety when you check out
the Abjad codebase. You may add to and edit the docs as soon as you 
download and install Abjad. However, to build HTML or PDF versions of the
docs and see the results of your changes you will first need to download
and install `Sphinx <http://sphinx.pocoo.org/>`_, the automated documentation
build and management system used by Abjad and a `number of other Python
projects <http://sphinx.pocoo.org/examples.html>`_, including www.python.org.

This remaining sections of this chapter describe how to find and edit the
Abjad docs, and how to build the the docs with Sphinx.


Layout of the docs
------------------

To see that the Abjad docs are included when you download the codebase,
change to ``ABJADPATH`` [#]_ and list the contents of that directory. ::

   abjad$ ls

   __init__.py   cluster       hairpin       octavation    spanner
   __init__.pyc  comments      harmonic      offset        staff
   accidental    component     instrument    override      staffgroup
   articulations container     interfaces    parentage     stem
   barline       context       layout        pianopedal    templates
   barnumber     core          leaf          pitch         tempo
   beam          debug         lily          rational      text
   book          demos         markup        receipt       thread
   bracket       directives    measure       rest          tie
   brackets      documentation meter         scm           tools
   breaks        dots          metricgrid    score         tremolo
   cfg           dynamics      navigator     scr           trill
   checks        exceptions    note          skip          tuplet
   chord         glissando     notehead      slur          update
   clef          grace         numbering     spacing       voice

The ``documentation`` directory lists together with the rest of the code.

Most of the contents of the ``documentation`` directory predates the 
Sphinx version of the site and can be ignored for this reason. 
Instead, list the contents of the ``documentation/doc_sphinx`` directory 
and take a look around. ::

   abjad$ ls documentation/doc_sphinx/

   Makefile   _templates chapters   index.rst  scr
   _static    _themes    conf.py    make.bat

The ``documentation/doc_sphinx`` directory contains everything 
required to build HTML, LaTeX and PDF versions of documentation system
for all of Abjad. The core content of the system lives in the 
``documentation/doc_sphinx/chapters`` subdirectory. ::

   abjad$ ls documentation/doc_sphinx/chapters/

   api               duration          lcs               standards
   bibliography      examples          note_basics       threads
   community         glossary          notehead          tour
   developers        grobhandlers      pitch             whatnext
   download          introduction      pitch_conventions

What you'll find as you inspect the chapters directories, or as you 
consider adding a new chapter directory, are a collection of ``.rst`` 
files organized into directories. The ``.rst`` extension identifies files
written in restructured text, or reST, described more fully below. ::

   abjad$ ls documentation/doc_sphinx/chapters/note_basics

   images        index.rst     index.rst.raw


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

.. [#] Abjad stores the location of Abjad codebase in the ``ABJADPATH``
   configuration variable. Note that ``ABJADPATH`` is not an OS-level
   environment variable but instead a configuration variable internal
   to Abjad. To see the value of ``ABJADPATH``, and find out where
   you installed Abjad after download, just type
   ``from abjad.cfg.cfg import ABJADPATH`` at the Abjad interpreter.
