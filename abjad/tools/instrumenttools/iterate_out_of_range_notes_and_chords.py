# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate


def iterate_out_of_range_notes_and_chords(expr):
    '''Iterates notes and chords in `expr` 
    outside traditional instrument ranges:

    ::

        >>> staff = Staff("c'8 r8 <d fs>8 r8")
        >>> violin = instrumenttools.Violin()
        >>> attach(violin, staff)

    ::

        >>> list(
        ... instrumenttools.iterate_out_of_range_notes_and_chords(
        ... staff))
        [Chord('<d fs>8')]

    Returns generator.
    '''
    from abjad.tools import instrumenttools

    component_classes = (scoretools.Note, scoretools.Chord)
    for note_or_chord in iterate(expr).by_class(component_classes):
        instrument = note_or_chord._get_effective_context_mark(
            instrumenttools.Instrument)
        if instrument is None:
            message = 'no instrument found.'
            raise ValueError(message)
        if note_or_chord not in instrument._default_pitch_range:
            yield note_or_chord
