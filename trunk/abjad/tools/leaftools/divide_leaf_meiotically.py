from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools import durationtools
import math


def divide_leaf_meiotically(leaf, n = 2):
    r'''.. versionadded:: 1.1

    Divide `leaf` meiotically `n` times::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        abjad> leaftools.divide_leaf_meiotically(staff[0], n = 4)

    ::

        abjad> f(staff)
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

    # TODO: find a way to optimize this; either reimplement
    # componenttools.extend_in_parent_of_component_and_grow_spanners()
    # or come up with something else.

    assert isinstance(leaf, _Leaf)
    assert mathtools.is_nonnegative_integer_power_of_two(n)
    assert 0 < n

    new_leaves = componenttools.copy_components_and_remove_all_spanners([leaf], n - 1)
    componenttools.extend_in_parent_of_component_and_grow_spanners(leaf, new_leaves)
    adjustment_multiplier = durationtools.Duration(1, n)
    leaf.written_duration *= adjustment_multiplier
    for new_leaf in new_leaves:
        new_leaf.written_duration *= adjustment_multiplier
