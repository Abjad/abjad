from abjad.tools import contexttools
from abjad.tools import iterationtools
from abjad.tools import pitchtools
from abjad.tools import voicetools


def notes_and_chords_in_expr_are_within_traditional_instrument_ranges(expr):
    '''.. versionadded:: 2.0

    True when notes and chords in `expr` are within traditional instrument ranges::

        >>> staff = Staff("c'8 r8 <d' fs'>8 r8")
        >>> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        >>> instrumenttools.notes_and_chords_in_expr_are_within_traditional_instrument_ranges(
        ...     staff)
        True

    False otherwise::

        >>> staff = Staff("c'8 r8 <d fs>8 r8")
        >>> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        >>> instrumenttools.notes_and_chords_in_expr_are_within_traditional_instrument_ranges(
        ...     staff)
        False

    Return boolean.
    '''

    for note_or_chord in iterationtools.iterate_notes_and_chords_in_expr(expr):
        instrument = contexttools.get_effective_instrument(note_or_chord)
        if note_or_chord not in instrument.traditional_pitch_range:
            return False
    else:
        return True
