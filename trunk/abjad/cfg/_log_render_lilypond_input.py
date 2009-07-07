from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg._get_next_output import _get_next_output
from abjad.cfg._run_lilypond import _run_lilypond
from abjad.cfg._verify_output_directory import _verify_output_directory
from abjad.cfg._wrap_format import _wrap_format
from abjad.cfg._write_footer import _write_footer
from abjad.cfg._write_preamble import _write_preamble
from abjad.cfg._write_title import _write_title
import os
import time


def _log_render_lilypond_input(expr, template = None, 
   title = None, footer = None, lilytime = 10):
   '''Private function that stores both .ly and .pdf files in the
   ABJADOUTPUT directory. Returns the name of the newly created file.
   '''

   current_directory = os.path.abspath('.')
   ## log score
   _verify_output_directory(ABJADOUTPUT)
   os.chdir(ABJADOUTPUT)
   name = _get_next_output( )
   outfile = open(name, 'w')
   _write_preamble(outfile, template)
   _write_title(outfile, title)
   _write_footer(outfile, footer)
   outfile.write(_wrap_format(expr.format))
   outfile.close( )
   ## render
   start_time = time.time( )
   _run_lilypond(name)
   stop_time = time.time( )
   total_time = int(stop_time - start_time)

   os.chdir(current_directory)

   if lilytime <= total_time:
      print 'LilyPond processing time equal to %s sec.' % total_time

   return name
