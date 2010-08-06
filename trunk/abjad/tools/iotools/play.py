from abjad.cfg._get_next_output import _get_next_output
from abjad.cfg._open_file import _open_file
from abjad.cfg._read_config_file import _read_config_file
from abjad.cfg._run_lilypond import _run_lilypond
from abjad.cfg._verify_output_directory import _verify_output_directory
from abjad.cfg._wrap_format_in_score_block import _wrap_format_in_score_block
from abjad.cfg._write_preamble import _write_preamble
from abjad.cfg._write_title import _write_title
import os


def play(expr):
   '''Call ``play(expr)`` to render Abjad expression ``expr`` as MIDI \
      and then open with the cross-platform file-opener.

      ::

         abjad> t = Note(0, (1, 4))
         abjad> play(t)

      This input renders and then opens a one-note MIDI file.

      *  Abjad outputs MIDI files of the format \
         ``filename.mid`` under Windows.
      *  Abjad outputs MIDI files of the format \
         ``filename.midi`` under other operating systems.
   '''

   ABJADOUTPUT = _read_config_file( )['abjad_output']
   _verify_output_directory(ABJADOUTPUT)
   os.chdir(ABJADOUTPUT)
   name = _get_next_output( )
   outfile = open(name, 'w')
   _write_preamble(outfile, None)
   outfile.write(_wrap_format_in_score_block(expr.format, midi=True))
   outfile.close( )
   _run_lilypond(name)
   if os.name == 'nt':
      extension = 'mid'
   else:
      extension = 'midi'
   midi_player = _read_config_file( )['midi_player']
   _open_file('%s.%s' % (name[:-3], extension), midi_player)
