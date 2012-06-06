from abjad.tools.tietools.TieSpanner import TieSpanner
from abjad.tools.tietools.get_tie_chain import get_tie_chain


def iterate_pitched_tie_chains_backward_in_expr(expr):
    r'''.. versionadded:: 2.9

    Iterate pitched tie chains backward in `expr`::

        >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 r8 f'8 ~ f'16 r8.")

    ::

        >>> f(staff)
        \new Staff {
            c'4 ~
            \times 2/3 {
                c'16
                d'8
            }
            e'8
            r8
            f'8 ~
            f'16
            r8.
        }

    ::

        >>> for x in tietools.iterate_pitched_tie_chains_backward_in_expr(staff): x
        ... 
        TieChain((Note("f'8"), Note("f'16")))
        TieChain((Note("e'8"),))
        TieChain((Note("d'8"),))
        TieChain((Note("c'4"), Note("c'16")))

    Tie chains are pitched if they comprise notes or chords.

    Tie chains are not pitched if they comprise rests or skips.

    Return generator.
    '''
    from abjad.tools import leaftools
    from abjad.tools import spannertools

    for leaf in leaftools.iterate_notes_and_chords_backward_in_expr(expr):
        tie_spanners = spannertools.get_spanners_attached_to_component(leaf, TieSpanner)
        if not tie_spanners or tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
            yield get_tie_chain(leaf)
