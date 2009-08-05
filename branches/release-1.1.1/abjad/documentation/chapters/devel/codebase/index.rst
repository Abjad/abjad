Codebase
========


How the Abjad codebase is laid out
----------------------------------

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

The remaining sections of this chapter cover the topics necessary
to familiarize developers coming to the project for the first time.


Installing the development version
----------------------------------

If you'd like to be at the cutting edge of the Abjad development 
you should install Subversion on your local machine,
check out from Google Code,
and then tell Python and your operating system about Abjad.

1. Install `Subversion <http://subversion.tigris.org>`_. 
   
   You can check to see if Subversion is already installed 
   on your machine first. ::

      svn help

   If Subversion responds then it is already installed.
   Otherwise visit the Subversion website.

2. Check out the Abjad codebase. ::

      svn checkout http://abjad.googlecode.com/svn/abjad/ abjad-read-only

3. Make the Python interpreter aware of Abjad. Symlink your Python 
   ``site-packages/`` directory to the ``abjad-read-only/`` directory. [#]_ ::

      ln -s /path/to/abjad-read-only SITE-PACKAGES-DIR/abjad

4. Alternatively, you can include the ``abjad-read-only`` directory in
   your ``PYTHONPATH`` environment variable. ::

      export PYTHONPATH="/path/to/abjad-read-only:"$PYTHONPATH

5. Finally, add the ``abjad-read-only/scr/`` directory to your ``PATH``. ::

      export PATH="/path/to/abjad-read-only/scr:"$PATH

   You will then be able to run Abjad directly with the ``abj`` command.

.. rubric:: Notes

.. [#] ``SITE-PACKAGES-DIR`` should be the Python 
   ``site-packages/`` directory.
   The Linux ``site-packages/`` directory is usually 
   ``/usr/lib/python2.x/site-packages``.
