from abjad.tools import spannertools


def iterate_pitched_tie_chains_in_expr(expr, reverse=False):
    r'''.. versionadded:: 2.10

    Iterate pitched tie chains forward in `expr`::

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

        >>> for x in tietools.iterate_pitched_tie_chains_in_expr(staff):
        ...     x
        ... 
        TieChain((Note("c'4"), Note("c'16")))
        TieChain((Note("d'8"),))
        TieChain((Note("e'8"),))
        TieChain((Note("f'8"), Note("f'16")))

    Iterate pitched tie chains backward in `expr`::

    ::

        >>> for x in tietools.iterate_pitched_tie_chains_in_expr(staff, reverse=True):
        ...     x
        ... 
        TieChain((Note("f'8"), Note("f'16")))
        TieChain((Note("e'8"),))
        TieChain((Note("d'8"),))
        TieChain((Note("c'4"), Note("c'16")))

    Tie chains are pitched if they comprise notes or chords.

    Tie chains are not pitched if they comprise rests or skips.

    Return generator.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import tietools

    if not reverse:
        for leaf in iterationtools.iterate_notes_and_chords_in_expr(expr):
            tie_spanners = spannertools.get_spanners_attached_to_component(leaf, tietools.TieSpanner)
            if not tie_spanners or tuple(tie_spanners)[0]._is_my_last_leaf(leaf):
                yield tietools.get_tie_chain(leaf)
    else:
        for leaf in iterationtools.iterate_notes_and_chords_in_expr(expr, reverse=True):
            tie_spanners = spannertools.get_spanners_attached_to_component(leaf, tietools.TieSpanner)
            if not tie_spanners or tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
                yield tietools.get_tie_chain(leaf)

