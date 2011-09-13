#from abjad.tools.divide._tie_chain_arbitrarily import _tie_chain_arbitrarily
from abjad.tools.tietools._tie_chain_to_tuplet import _tie_chain_to_tuplet


def tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots(tie_chain, proportions):
    r'''.. versionadded:: 2.0

    Divide `tie_chain` into fixed-duration tuplet according to
    arbitrary integer `proportions`.

    Interpret `proportions` as a ratio. That is, reduce integers
    in `proportions` relative to each other.

    Return non-trivial tuplet as diminution.

    Where ``proportions[i] == 1`` for ``i < len(proportions)``,
    do not allow tupletted notes to carry dots. ::

        abjad> staff = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
        abjad> tietools.TieSpanner(staff[:2])
        TieSpanner(c'8, c'16)
        abjad> spannertools.BeamSpanner(staff[:])
        BeamSpanner(c'8, c'16, c'16)
        abjad> tie_chain = tietools.get_tie_chain(staff[0])
        abjad> tietools.tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots(tie_chain, [1])
        FixedDurationTuplet(3/16, [c'4])
        abjad> f(staff)
        \new Staff {
            \fraction \times 3/4 {
                c'4 [
            }
            c'16 ]
        }

    ::

        abjad> staff = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
        abjad> tietools.TieSpanner(staff[:2])
        TieSpanner(c'8, c'16)
        abjad> spannertools.BeamSpanner(staff[:])
        BeamSpanner(c'8, c'16, c'16)
        abjad> tie_chain = tietools.get_tie_chain(staff[0])
        abjad> tietools.tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots(tie_chain, [1, 2])
        FixedDurationTuplet(3/16, [c'16, c'8])
        abjad> f(staff)
        \new Staff {
            {
                c'16 [
                c'8
            }
            c'16 ]
        }

    ::

        abjad> staff = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
        abjad> tietools.TieSpanner(staff[:2])
        TieSpanner(c'8, c'16)
        abjad> spannertools.BeamSpanner(staff[:])
        BeamSpanner(c'8, c'16, c'16)
        abjad> tie_chain = tietools.get_tie_chain(staff[0])
        abjad> tietools.tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots(tie_chain, [1, 2, 2])
        FixedDurationTuplet(3/16, [c'16, c'8, c'8])
        abjad> f(staff)
        \new Staff {
            \fraction \times 3/5 {
                c'16 [
                c'8
                c'8
            }
            c'16 ]
        }

    .. versionchanged:: 2.0
        renamed ``divide.tie_chain_into_arbitrary_diminution_undotted()`` to
        ``tietools.tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots()``.
    '''

    prolation, dotted = 'diminution', False
    #return _tie_chain_arbitrarily(tie_chain, proportions, prolation, dotted)
    return _tie_chain_to_tuplet(tie_chain, proportions, prolation, dotted)
