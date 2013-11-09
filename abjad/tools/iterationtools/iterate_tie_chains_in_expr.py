# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.topleveltools import iterate


def iterate_tie_chains_in_expr(expr, reverse=False):
    r'''Iterate tie chains forward in `expr`:

    ::

        >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")

    ..  doctest::

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

        >>> for x in iterationtools.iterate_tie_chains_in_expr(staff):
        ...     x
        ...
        TieChain(Note("c'4"), Note("c'16"))
        TieChain(Note("d'8"),)
        TieChain(Note("e'8"),)
        TieChain(Note("f'4"), Note("f'16"))

    Iterate tie chains backward in `expr`:

    ::

        >>> for x in iterationtools.iterate_tie_chains_in_expr(staff, reverse=True):
        ...     x
        ...
        TieChain(Note("f'4"), Note("f'16"))
        TieChain(Note("e'8"),)
        TieChain(Note("d'8"),)
        TieChain(Note("c'4"), Note("c'16"))

    Returns generator.
    '''

    spanner_classes = (spannertools.Tie, )
    if not reverse:
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            tie_spanners = leaf._get_spanners(spanner_classes)
            if not tie_spanners or \
                tuple(tie_spanners)[0]._is_my_last_leaf(leaf):
                yield leaf._get_tie_chain()
    else:
        for leaf in iterate(expr).by_class(scoretools.Leaf, reverse=True):
            tie_spanners = leaf._get_spanners(spanner_classes)
            if not(tie_spanners) or \
                tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
                yield leaf._get_tie_chain()
