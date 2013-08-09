# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools import voicetools
from abjad.tools.selectiontools import more


def iterate_notes_and_chords_in_expr_outside_traditional_instrument_ranges(expr):
    '''Iterate notes and chords in `expr` outside traditional instrument ranges:

    ::

        >>> staff = Staff("c'8 r8 <d fs>8 r8")
        >>> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        >>> list(
        ... instrumenttools.iterate_notes_and_chords_in_expr_outside_traditional_instrument_ranges(
        ... staff))
        [Chord('<d fs>8')]

    Return generator.
    '''
    from abjad.tools import iterationtools

    for note_or_chord in iterationtools.iterate_notes_and_chords_in_expr(expr):
        instrument = note_or_chord._get_effective_context_mark(
            contexttools.InstrumentMark)
        if instrument is None:
            raise MissingInstrumentError
        if note_or_chord not in instrument.default_pitch_range:
            yield note_or_chord
