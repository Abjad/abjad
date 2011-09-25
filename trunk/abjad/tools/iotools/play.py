from abjad.cfg._read_config_file import _read_config_file
from abjad.tools import lilypondfiletools
from abjad.tools.iotools._insert_expr_into_lilypond_file import _insert_expr_into_lilypond_file
from abjad.tools.iotools._open_file import _open_file
from abjad.tools.iotools._run_lilypond import _run_lilypond
from abjad.tools.iotools._verify_output_directory import _verify_output_directory
from abjad.tools.iotools.get_next_output_file_name import get_next_output_file_name
import os


def play(expr):
    '''Play `expr`::

        abjad> note = Note("c'4")

    ::

        abjad> iotools.play(note) # doctest: +SKIP

    This input creates and opens a one-note MIDI file.

    Abjad outputs MIDI files of the format ``filename.mid`` under Windows.

    Abjad outputs MIDI files of the format ``filename.midi`` under other operating systems.
    '''

    ABJADOUTPUT = _read_config_file()['abjad_output']
    _verify_output_directory(ABJADOUTPUT)
    os.chdir(ABJADOUTPUT)
    name = get_next_output_file_name()
    outfile = open(name, 'w')
    lilypond_file = _insert_expr_into_lilypond_file(expr)
    lilypond_file.score_block.append(lilypondfiletools.MIDIBlock())
    outfile.write(lilypond_file.format)
    outfile.close()
    _run_lilypond(name, _read_config_file()['lilypond_path'])
    if os.name == 'nt':
        extension = 'mid'
    else:
        extension = 'midi'
    midi_player = _read_config_file()['midi_player']
    _open_file('%s.%s' % (name[:-3], extension), midi_player)
