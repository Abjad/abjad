from abjad.tools import leaftools
from abjad.tools import spannertools


def iterate_nontrivial_tie_chains_backward_in_expr(expr):
    r'''Iterate nontrivial tie chains backward in `expr`::

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

        >>> for x in tietools.iterate_nontrivial_tie_chains_backward_in_expr(staff):
        ...     x
        ...
        TieChain((Note("f'4"), Note("f'16")))
        TieChain((Note("c'4"), Note("c'16")))

    Return generator.
    '''
    from abjad.tools import tietools

    for leaf in leaftools.iterate_leaves_backward_in_expr(expr):
        tie_spanners = spannertools.get_spanners_attached_to_component(leaf, tietools.TieSpanner)
        if not(tie_spanners) or tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
            tie_chain = tietools.get_tie_chain(leaf)
            if not tie_chain.is_trivial:
                yield tie_chain
