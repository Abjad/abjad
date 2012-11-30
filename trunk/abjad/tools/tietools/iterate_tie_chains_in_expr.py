from abjad.tools import spannertools


def iterate_tie_chains_in_expr(expr, reverse=False):
    r'''Iterate tie chains forward in `expr`::

        >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")

    ::

        >>> f(staff)
        \new Staff {
            c'4 ~
            \times 2/3 {
                c'16
                d'8
            }
            e'8
            f'4 ~
            f'16
        }

    ::

        >>> for x in tietools.iterate_tie_chains_in_expr(staff):
        ...     x
        ...
        TieChain(Note("c'4"), Note("c'16"))
        TieChain(Note("d'8"),)
        TieChain(Note("e'8"),)
        TieChain(Note("f'4"), Note("f'16"))

    Iterate tie chains backward in `expr`::

    ::

        >>> for x in tietools.iterate_tie_chains_in_expr(staff, reverse=True):
        ...     x
        ...
        TieChain(Note("f'4"), Note("f'16"))
        TieChain(Note("e'8"),)
        TieChain(Note("d'8"),)
        TieChain(Note("c'4"), Note("c'16"))

    Return generator.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import tietools

    if not reverse:
        for leaf in iterationtools.iterate_leaves_in_expr(expr):
            tie_spanners = spannertools.get_spanners_attached_to_component(leaf, tietools.TieSpanner)
            if not tie_spanners or tuple(tie_spanners)[0]._is_my_last_leaf(leaf):
                yield tietools.get_tie_chain(leaf)
    else:
        for leaf in iterationtools.iterate_leaves_in_expr(expr, reverse=True):
            tie_spanners = spannertools.get_spanners_attached_to_component(leaf, tietools.TieSpanner)
            if not(tie_spanners) or tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
                yield tietools.get_tie_chain(leaf)
