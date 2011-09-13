from abjad.tools import componenttools
from abjad.tools.leaftools.divide_leaf_meiotically import divide_leaf_meiotically
from abjad.tools.leaftools.iterate_leaves_backward_in_expr import iterate_leaves_backward_in_expr


def divide_leaves_in_expr_meiotically(expr, n = 2):
    r'''.. versionadded:: 1.1

    Divide leaves meiotically in `expr` `n` times::

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

        abjad> leaftools.divide_leaves_in_expr_meiotically(staff[2:], n = 4)

    ::

        abjad> f(staff)
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

    .. versionchanged:: 2.0
        renamed ``leaftools.meiose()`` to
        ``leaftools.divide_leaves_in_expr_meiotically()``.
    '''

    # can not wrap with update control because of          #
    # extend_in_parent_of_component_and_grow_spanners() #
    for leaf in iterate_leaves_backward_in_expr(expr):
        divide_leaf_meiotically(leaf, n)
