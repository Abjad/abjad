# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def repeat_leaf(leaf, total=1):
    r'''Repeat `leaf` and extend spanners:

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

        >>> leaftools.repeat_leaf(staff[0], total=3)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 [
            c'8
            c'8
            d'8
            e'8
            f'8 ]
        }

    Preserve `leaf` written duration.

    Preserve parentage and spanners.

    Return none.
    '''

    leaf._splice(
        componenttools.copy_components_and_detach_spanners([leaf], total - 1),
        grow_spanners=True,
        )
