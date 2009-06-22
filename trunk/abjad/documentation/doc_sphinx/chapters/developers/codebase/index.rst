The Abjad codebase
==================

The Abjad codebase comprises several dozen different Python packages that
together implement a formal model of the musical score. Abjad r2330 includes
73 top-level packages. ::

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

Some top-level packages then contain a number of nested packages inside. ::

   abjad$ ls beam/
   __init__.py   complex       format.pyc    interface.pyc spanner.pyc
   __init__.pyc  format.py     interface.py  spanner.py    test

::

   abjad$ ls beam/complex/
   __init__.py  durated      format.pyc   spanner.py   test
   __init__.pyc format.py    measured     spanner.pyc

::

   abjad$ ls beam/complex/durated/
   __init__.py  format.py    spanner.py   test
   __init__.pyc format.pyc   spanner.pyc

Understanding the difference between active Python packages and regular
directories on the filesystem is an important to understand the way
that the Abjad codebase in laid out. The remaining sections of this
chapter will cover the layout of the codebase together with the other
topics necessary to familiarize developers coming to the project for
the first time.
