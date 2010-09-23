from abjad.tools.iotools.get_last_output_file_name import get_last_output_file_name
from abjad.cfg._read_config_file import _read_config_file
import os


def save_last_ly_as(file_name):
   r'''.. versionadded:: 1.1.2

   Save last LilyPond file as `file_name`::

      abjad> show(score)
      abjad> lilyfiletools.save_last_ly_as('/project/output/example-1.ly')

   Return none.

   .. versionchanged:: 1.1.2
      renamed ``lilyfiletools.save_ly_as( )`` to
      ``lilyfiletools.save_last_ly_as( )``.
   '''

   ABJADOUTPUT = _read_config_file( )['abjad_output'] 
   last_ly = get_last_output_file_name( )
   last_ly_full_name = os.path.join(ABJADOUTPUT, last_ly)
   old = open(last_ly_full_name, 'r')
   new = open(file_name, 'w')
   new.write(''.join(old.readlines( )))
   old.close( )
   new.close( )
