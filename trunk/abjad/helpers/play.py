from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg.get_next_output import _get_next_output
from abjad.cfg.open_file import _open_file
from abjad.cfg.read_config_value import _read_config_value
from abjad.cfg.run_lilypond import _run_lilypond
from abjad.cfg.verify_output_directory import _verify_output_directory
from abjad.cfg.wrap_format_in_score_block import _wrap_format_in_score_block
from abjad.cfg.write_preamble import _write_preamble
from abjad.cfg.write_title import _write_title
import os


def play(ly):
   '''
   Renders a given Abjad expression and plays it with your 
   favorite MIDI player. 
   '''

   _verify_output_directory(ABJADOUTPUT)
   os.chdir(ABJADOUTPUT)
   name = _get_next_output( )
   outfile = open(name, 'w')
   _write_preamble(outfile, None)
   outfile.write(_wrap_format_in_score_block(ly.format, midi=True))
   outfile.close( )
   _run_lilypond(name)
   if os.name == 'nt':
      extension = 'mid'
   else:
      extension = 'midi'
   midiplayer = _read_config_value('midiplayer')
   _open_file('%s.%s' % (name[:-3], extension), midiplayer)

