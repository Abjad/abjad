from abjad.cfg._get_last_output import _get_last_output
from abjad.cfg._read_config_file import _read_config_file
import os


def save_pdf_as(file_name):
   r'''.. versionadded:: 1.1.2

   Save last PDF as `file_name`::

      abjad> show(score)
      abjad> lilytools.save_pdf_as('/project/output/example-1.pdf')

   Return none.
   '''

   ABJADOUTPUT = _read_config_file( )['abjad_output'] 
   last_ly = _get_last_output( )
   last_pdf = last_ly[:-3] + '.pdf'
   last_pdf_full_name = os.path.join(ABJADOUTPUT, last_pdf)
   old = open(last_pdf_full_name, 'r')
   new = open(file_name, 'w')
   new.write(''.join(old.readlines( )))
   old.close( )
   new.close( )
