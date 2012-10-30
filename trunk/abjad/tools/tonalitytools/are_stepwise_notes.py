from abjad.tools import iterationtools
from abjad.tools import notetools
from abjad.tools import pitchtools
from abjad.tools import sequencetools


def are_stepwise_notes(*expr):
    '''.. versionadded:: 2.0

    True when notes in `expr` are stepwise. ::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> tonalitytools.are_stepwise_notes(t[:])
        True

    Otherwise false. ::

        >>> tonalitytools.are_stepwise_notes(Note("c'4"), Note("c'4"))
        False

    .. versionchanged:: 2.0
        renamed ``tonalitytools.are_stepwise()`` to
        ``tonalitytools.are_stepwise_notes()``.
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
