# -*- encoding: utf-8 -*-
import os


def play(expr):
    r'''Plays `expr`.

    ::

        >>> note = Note("c'4")

    ::

        >>> topleveltools.play(note) # doctest: +SKIP

    This input creates and opens a one-note MIDI file.

    Abjad outputs MIDI files of the format ``filename.mid`` 
    under Windows.

    Abjad outputs MIDI files of the format ``filename.midi`` 
    under other operating systems.

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import lilypondfiletools
    from abjad.tools import systemtools
    ABJADOUTPUT = abjad_configuration['abjad_output']
    systemtools.IOManager.ensure_directory_existence(ABJADOUTPUT)
    os.chdir(ABJADOUTPUT)
    name = systemtools.IOManager.get_next_output_file_name()
    outfile = open(name, 'w')
    lilypond_file = systemtools.IOManager.insert_expr_into_lilypond_file(expr)
    lilypond_file.score_block.append(lilypondfiletools.MIDIBlock())
    outfile.write(format(lilypond_file))
    outfile.close()
    systemtools.IOManager.run_lilypond(name, abjad_configuration['lilypond_path'])
    if os.name == 'nt':
        extension = 'mid'
    else:
        extension = 'midi'
    midi_player = abjad_configuration['midi_player']
    systemtools.IOManager.open_file('%s.%s' % (name[:-3], extension), midi_player)
