from abjad.tools import configurationtools
from abjad.tools import lilypondfiletools
import os


def play(expr):
    '''Play `expr`::

        >>> note = Note("c'4")

    ::

        >>> iotools.play(note) # doctest: +SKIP

    This input creates and opens a one-note MIDI file.

    Abjad outputs MIDI files of the format ``filename.mid`` under Windows.

    Abjad outputs MIDI files of the format ``filename.midi`` under other operating systems.
    '''
    from abjad import ABJCFG
    from abjad.tools import iotools
    from abjad.tools.iotools._insert_expr_into_lilypond_file import _insert_expr_into_lilypond_file
    from abjad.tools.iotools._open_file import _open_file
    from abjad.tools.iotools._run_lilypond import _run_lilypond
    from abjad.tools.iotools._verify_output_directory import _verify_output_directory

    ABJADOUTPUT = ABJCFG['abjad_output']
    _verify_output_directory(ABJADOUTPUT)
    os.chdir(ABJADOUTPUT)
    name = iotools.get_next_output_file_name()
    outfile = open(name, 'w')
    lilypond_file = _insert_expr_into_lilypond_file(expr)
    lilypond_file.score_block.append(lilypondfiletools.MIDIBlock())
    outfile.write(lilypond_file.lilypond_format)
    outfile.close()
    _run_lilypond(name, ABJCFG['lilypond_path'])
    if os.name == 'nt':
        extension = 'mid'
    else:
        extension = 'midi'
    midi_player = ABJCFG['midi_player']
    #print midi_player
    #print '%s.%s' % (name[:-3], extension)
    _open_file('%s.%s' % (name[:-3], extension), midi_player)
