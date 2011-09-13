#from abjad.tools.divide._tie_chain_arbitrarily import _tie_chain_arbitrarily
from abjad.tools.tietools._tie_chain_to_tuplet import _tie_chain_to_tuplet


def tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots(tie_chain, proportions):
    r'''.. versionadded:: 2.0

    Divide `tie_chain` into fixed-duration tuplet according to
    arbitrary integer `proportions`.

    Interpret `proportions` as a ratio. That is, reduce integers
    in `proportions` relative to each other.

    Return non-trivial tuplet as diminution.

    Where ``proportions[i] == 1`` for ``i < len(proportions)``, allow
    tupletted notes to carry dots. ::

        abjad> staff = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
        abjad> tietools.TieSpanner(staff[:2])
        TieSpanner(c'8, c'16)
        abjad> spannertools.BeamSpanner(staff[:])
        BeamSpanner(c'8, c'16, c'16)
        abjad> tie_chain = tietools.get_tie_chain(staff[0])
        abjad> tietools.tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots(tie_chain, [1])
        FixedDurationTuplet(3/16, [c'8.])
        abjad> f(staff)
        \new Staff {
            {
                c'8. [
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
        abjad> tietools.tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots(tie_chain, [1, 2])
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
        abjad> tietools.tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots(tie_chain, [1, 2, 2])
        FixedDurationTuplet(3/16, [c'32., c'16., c'16.])
        abjad> f(staff)
        \new Staff {
            \times 4/5 {
                c'32. [
                c'16.
                c'16.
            }
            c'16 ]
        }

    .. versionchanged:: 2.0
        renamed ``divide.tie_chain_into_arbitrary_diminution_dotted()`` to
        ``tietools.tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots()``.
    '''

    prolation, dotted = 'diminution', True
    #return _tie_chain_arbitrarily(tie_chain, proportions, prolation, dotted)
    return _tie_chain_to_tuplet(tie_chain, proportions, prolation, dotted)
