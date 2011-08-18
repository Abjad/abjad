from abjad.tools.notetools.Note import Note
from abjad.tools import componenttools
from abjad.tools import pitchtools
from abjad.tools import seqtools


def are_stepwise_ascending_notes(*expr):
    '''.. versionadded:: 2.0

    True when notes in `expr` are stepwise ascneding. ::

        abjad> from abjad.tools import tonalitytools

    ::

        abjad> t = Staff("c'8 d'8 e'8 f'8")
        abjad> tonalitytools.are_stepwise_ascending_notes(t[:])
        True

    Otherwise false. ::

        abjad> tonalitytools.are_stepwise_ascending_notes(Note("c'4"), Note("c'4"))
        False

    .. versionchanged:: 2.0
        renamed ``tonalitytools.are_stepwise_ascending()`` to
        ``tonalitytools.are_stepwise_ascending_notes()``.
    '''

    for left, right in seqtools.iterate_sequence_pairwise_strict(
        componenttools.iterate_components_forward_in_expr(expr, Note)):
        try:
            assert not (left.written_pitch == right.written_pitch)
            mdi = pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(left, right)
            assert mdi.number == 2
        except AssertionError:
            return False

    return True
