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
