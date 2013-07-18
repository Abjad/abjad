from abjad.tools import iterationtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from abjad.tools.selectiontools.Selection import Selection


class TonalAnalysisSelection(Selection):
    r'''Tonal analysis selection.

    ::

        >>> staff = Staff("c'4 d' e' f'")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> selection_1 = tonalanalysistools.select(staff[:])

    ::

        >>> z(selection_1)
        tonalanalysistools.TonalAnalysisSelection(
            music=(Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4"))
            )

    Example 2. Disjunct selection:

    ::

        >>> notes = (staff[0], staff[3])
        >>> selection_2 = tonalanalysistools.select(notes)

    ::

        >>> z(selection_2)
        tonalanalysistools.TonalAnalysisSelection(
            music=(Note("c'4"), Note("f'4"))
            )

    '''


    def are_scalar_notes(self):
        '''True when notes in selection are scalar:

        ::

            >>> selection_1.are_scalar_notes()
            True

        Otherwise false:

        ::


            >>> selection_2.are_scalar_notes()
            False

        Return boolean.
        '''
        direction_string = None
        for left, right in sequencetools.iterate_sequence_pairwise_strict(
            iterationtools.iterate_notes_in_expr(self)):
            try:
                assert not (left.written_pitch == right.written_pitch)
                mdi = pitchtools.calculate_melodic_diatonic_interval(
                    left, right)
                assert mdi.number <= 2
                if direction_string is None:
                    direction_string = mdi.direction_string
                assert direction_string == mdi.direction_string
            except AssertionError:
                return False
        return True
