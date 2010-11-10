from abjad.cfg._read_config_file import _read_config_file
import os


## TODO: Call operating-specific view program instead of vi. ##

def log( ):
   '''Open the LilyPond log file in the ``vi``::

      abjad> iotools.log( )

   ::

      GNU LilyPond 2.12.2
      Processing `0440.ly'
      Parsing...
      Interpreting music...
      Preprocessing graphical objects...
      Finding the ideal number of pages...
      Fitting music on 1 page...
      Drawing systems...
      Layout output to `0440.ps'...
      Converting to `./0440.pdf'...         

   Exit ``vi`` in the usual way with ``:q`` or equivalent to return to the Abjad interpreter.

   Return none.
   '''

   ABJADOUTPUT = _read_config_file( )['abjad_output']
   os.system('vi %s' % os.path.join(ABJADOUTPUT, 'lily.log'))
