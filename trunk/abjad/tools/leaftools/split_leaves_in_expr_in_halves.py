# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def split_leaves_in_expr_in_halves(expr, n=2):
    r'''Divide leaves meiotically in `expr` `n` times:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> spannertools.BeamSpanner(staff.select_leaves())
        BeamSpanner(c'8, d'8, e'8, f'8)
        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> leaftools.split_leaves_in_expr_in_halves(staff[2:], n=4)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'32
            e'32
            e'32
            e'32
            f'32
            f'32
            f'32
            f'32 ]
        }

    Replace every leaf in `expr` with `n` new leaves.

    Preserve parentage and spanners.

    Allow divisions into only ``1, 2, 4, 8, 16, ...`` and other
    nonnegative integer powers of ``2``.

    Produce only leaves and never tuplets or other containers.

    Return none.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import leaftools

    # can not wrap with update control because of self._splice()
    for leaf in iterationtools.iterate_leaves_in_expr(expr, reverse=True):
        leaftools.split_leaf_in_halves(leaf, n)
