# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import mathtools


def divide_leaf_meiotically(leaf, n=2):
    r'''Divide `leaf` meiotically `n` times:

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

        >>> leaftools.divide_leaf_meiotically(staff[0], n=4)

    ::

        >>> f(staff)
        \new Staff {
            c'32 [
            c'32
            c'32
            c'32
            d'8
            e'8
            f'8 ]
        }


    Replace `leaf` with `n` new leaves.

    Preserve parentage and spanners.

    Allow divisions into only ``1, 2, 4, 8, 16, ...`` and other
    nonnegative integer powers of ``2``.

    Produce only leaves and never tuplets or other containers.

    Return none.
    '''
    from abjad.tools import leaftools

    # TODO: find a way to optimize this; either reimplement
    #       self.extend_in_parent() or come up with something else.

    assert isinstance(leaf, leaftools.Leaf)
    assert mathtools.is_nonnegative_integer_power_of_two(n)
    assert 0 < n

    new_leaves = componenttools.copy_components_and_detach_spanners(
        [leaf], n - 1)
    leaf.extend_in_parent(new_leaves, grow_spanners=True)
    adjustment_multiplier = durationtools.Duration(1, n)
    leaf.written_duration *= adjustment_multiplier
    for new_leaf in new_leaves:
        new_leaf.written_duration *= adjustment_multiplier
