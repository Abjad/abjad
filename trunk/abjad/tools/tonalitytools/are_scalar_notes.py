from abjad.tools import iterationtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools


def are_scalar_notes(*expr):
    '''.. versionadded:: 2.0

    True when notes in `expr` are scalar. ::

        >>> from abjad.tools import tonalitytools

    ::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> tonalitytools.are_scalar_notes(t[:])
        True

    Otherwise false. ::

        >>> tonalitytools.are_scalar_notes(Note("c'4"), Note("c'4"))
        False

    .. versionchanged:: 2.0
        renamed ``tonalitytools.are_scalar()`` to
        ``tonalitytools.are_scalar_notes()``.
    '''

    direction_string = None
    for left, right in sequencetools.iterate_sequence_pairwise_strict(
        iterationtools.iterate_notes_in_expr(expr)):
        try:
            assert not (left.written_pitch == right.written_pitch)
            mdi = pitchtools.calculate_melodic_diatonic_interval(left, right)
            assert mdi.number <= 2
            if direction_string is None:
                direction_string = mdi.direction_string
            assert direction_string == mdi.direction_string
        except AssertionError:
            return False

    return True
