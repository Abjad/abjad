from abjad.tools import pitchtools
from abjad.tools import voicetools
from abjad.tools.contexttools.get_effective_instrument import get_effective_instrument


def notes_and_chords_in_expr_are_within_traditional_instrument_ranges(expr):
    '''.. versionadded:: 2.0

    True when notes and chords in `expr` are within traditional instrument ranges::

        abjad> staff = Staff("c'8 r8 <d' fs'>8 r8")
        abjad> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        abjad> instrumenttools.notes_and_chords_in_expr_are_within_traditional_instrument_ranges(staff)
        True

    False otherwise::

        abjad> staff = Staff("c'8 r8 <d fs>8 r8")
        abjad> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        abjad> instrumenttools.notes_and_chords_in_expr_are_within_traditional_instrument_ranges(staff)
        False

    Return boolean.
    '''
    from abjad.tools import leaftools

    for note_or_chord in leaftools.iterate_notes_and_chords_forward_in_expr(expr):
        instrument = get_effective_instrument(note_or_chord)
        if note_or_chord not in instrument.traditional_pitch_range:
            return False
    else:
        return True
