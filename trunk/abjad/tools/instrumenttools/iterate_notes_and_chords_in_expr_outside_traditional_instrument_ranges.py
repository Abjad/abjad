from abjad.tools import pitchtools
from abjad.tools import voicetools
from abjad.tools.contexttools.get_effective_instrument import get_effective_instrument


def iterate_notes_and_chords_in_expr_outside_traditional_instrument_ranges(expr):
    '''.. versionadded:: 2.0

    Iterate notes and chords in `expr` outside traditional instrument ranges::

        abjad> staff = Staff("c'8 r8 <d fs>8 r8")
        abjad> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        abjad> for note_or_chord in instrumenttools.iterate_notes_and_chords_in_expr_outside_traditional_instrument_ranges(staff):
        ...   note_or_chord
        Chord('<d fs>8')

    Return generator.
    '''
    from abjad.tools import leaftools

    for note_or_chord in leaftools.iterate_notes_and_chords_forward_in_expr(expr):
        instrument = get_effective_instrument(note_or_chord)
        if instrument is None:
            raise MissingInstrumentError
        if note_or_chord not in instrument.traditional_pitch_range:
            yield note_or_chord
