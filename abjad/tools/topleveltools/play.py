# -*- coding: utf-8 -*-
import os


def play(expr):
    r'''Plays `expr`.

    ::

        >>> note = Note("c'4")

    ::

        >>> topleveltools.play(note) # doctest: +SKIP

    This input creates and opens a one-note MIDI file.

    Abjad outputs MIDI files of the format ``file_name.mid``
    under Windows.

    Abjad outputs MIDI files of the format ``file_name.midi``
    under other operating systems.

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import systemtools
    from abjad.tools import topleveltools
    assert hasattr(expr, '__illustrate__')
    midi_file_path, abjad_formatting_time, lilypond_rendering_time = \
        topleveltools.persist(expr).as_midi()
    midi_player = abjad_configuration['midi_player']
    systemtools.IOManager.open_file(midi_file_path, midi_player)
