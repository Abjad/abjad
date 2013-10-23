# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools import voicetools


def iterate_out_of_range_notes_and_chords(expr):
    '''Iterates notes and chords in `expr` 
    outside traditional instrument ranges:

    ::

        >>> staff = Staff("c'8 r8 <d fs>8 r8")
        >>> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        >>> list(
        ... instrumenttools.iterate_out_of_range_notes_and_chords(
        ... staff))
        [Chord('<d fs>8')]

    Returns generator.
    '''
    from abjad.tools import instrumenttools
    from abjad.tools import iterationtools

    for note_or_chord in iterationtools.iterate_notes_and_chords_in_expr(expr):
        instrument = note_or_chord._get_effective_context_mark(
            instrumenttools.Instrument)
        if instrument is None:
            raise MissingInstrumentError
        if note_or_chord not in instrument._default_pitch_range:
            yield note_or_chord
