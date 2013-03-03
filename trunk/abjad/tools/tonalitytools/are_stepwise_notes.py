from abjad.tools import iterationtools
from abjad.tools import notetools
from abjad.tools import pitchtools
from abjad.tools import sequencetools


def are_stepwise_notes(*expr):
    '''.. versionadded:: 2.0

    True when notes in `expr` are stepwise:

    ::

        >>> staff = Staff("c'8 ( d' e' d' ) c'4")
        >>> time_signature = contexttools.TimeSignatureMark((3, 4))(staff)

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> tonalitytools.are_stepwise_notes(staff)
        True

    Otherwise false:

    ::

        >>> staff[-1] = "g'4"

    ::
    
        >>> show(staff) # doctest: +SKIP

    ::

        >>> tonalitytools.are_stepwise_notes(staff)
        False

    Return boolean.
    '''

    for left, right in sequencetools.iterate_sequence_pairwise_strict(
        iterationtools.iterate_notes_in_expr(expr)):
        try:
            assert not (left.written_pitch == right.written_pitch)
            hdi = pitchtools.calculate_harmonic_diatonic_interval(left, right)
            assert hdi.number <= 2
        except AssertionError:
            return False

    return True
