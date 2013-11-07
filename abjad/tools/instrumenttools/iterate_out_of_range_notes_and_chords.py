# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import pitchtools
from abjad.tools import scoretools


def iterate_out_of_range_notes_and_chords(expr):
    '''Iterates notes and chords in `expr` 
    outside traditional instrument ranges:

    ::

        >>> staff = Staff("c'8 r8 <d fs>8 r8")
        >>> violin = instrumenttools.Violin()
        >>> attach(violin, staff)
        Violin()(Staff{4})

    ::

        >>> list(
        ... instrumenttools.iterate_out_of_range_notes_and_chords(
        ... staff))
        [Chord('<d fs>8')]

    Returns generator.
    '''
    from abjad.tools import instrumenttools
    from abjad.tools.topleveltools import iterate

    for note_or_chord in iterate(expr).by_class(
        (scoretools.Note, scoretools.Chord)):
        instrument = note_or_chord._get_effective_context_mark(
            instrumenttools.Instrument)
        if instrument is None:
            raise MissingInstrumentError
        if note_or_chord not in instrument._default_pitch_range:
            yield note_or_chord
