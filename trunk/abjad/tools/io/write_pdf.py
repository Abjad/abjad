from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg.get_next_output import _get_next_output
from abjad.cfg.open_file import _open_file
from abjad.cfg.read_config_value import _read_config_value
from abjad.cfg.run_lilypond import _run_lilypond
from abjad.cfg.verify_output_directory import _verify_output_directory
from abjad.cfg.wrap_format import _wrap_format
from abjad.cfg.write_preamble import _write_preamble
from abjad.cfg.write_title import _write_title
import os
import time


## TODO: Remove massive code duplication with show( ). ##

def write_pdf(expr, file_name, template = None, title = None, lilytime = 10):
   '''Render ``expr`` as `LilyPond` input, call `LilyPond`
   and write the resulting PDF as ``file_name``::

      abjad> t = Note(0, (1, 4))
      abjad> write_pdf(t, 'one_note.pdf')'''

   current_directory = os.path.abspath('.')

   _verify_output_directory(ABJADOUTPUT)
   os.chdir(ABJADOUTPUT)
   name = _get_next_output( )
   outfile = open(name, 'w')
   _write_preamble(outfile, template)
   _write_title(outfile, title)
   outfile.write(_wrap_format(expr.format))
   outfile.close( )
   start_time = time.time( )
   _run_lilypond(name)
   stop_time = time.time( )
   total_time = int(stop_time - start_time)
   pdf_name = name[:-3] + '.pdf'
   full_file_name = os.path.join(current_directory, file_name)
   os.system('mv %s %s' % (pdf_name, full_file_name))
   if lilytime <= total_time:
      print 'LilyPond processing time equal to %s sec.' % total_time
   print 'LilyPond PDF written to %s.' % full_file_name
