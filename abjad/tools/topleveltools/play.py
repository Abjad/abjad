# -*- coding: utf-8 -*-
import os


def play(expr):
    r'''Plays `expr`.

    ..  container:: example

        ::

            >>> note = Note("c'4")
            >>> play(note) # doctest: +SKIP

    Makes MIDI file.

    Appends ``.mid`` filename extension under Windows.

    Appends ``.midi`` filename extension under other operating systems. 

    Opens MIDI file.

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import systemtools
    from abjad.tools import topleveltools
    assert hasattr(expr, '__illustrate__')
    result = topleveltools.persist(expr).as_midi()
    midi_file_path, abjad_formatting_time, lilypond_rendering_time = result
    midi_player = abjad_configuration['midi_player']
    systemtools.IOManager.open_file(midi_file_path, midi_player)
