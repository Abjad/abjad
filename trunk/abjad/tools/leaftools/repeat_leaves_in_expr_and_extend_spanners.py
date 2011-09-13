from abjad.tools.leaftools.iterate_leaves_backward_in_expr import iterate_leaves_backward_in_expr
from abjad.tools.leaftools.repeat_leaf_and_extend_spanners import repeat_leaf_and_extend_spanners


def repeat_leaves_in_expr_and_extend_spanners(expr, total = 1):
    r'''.. versionadded:: 1.1

    Repeat leaves in `expr` and extend spanners::

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

        abjad> result = leaftools.repeat_leaves_in_expr_and_extend_spanners(staff[2:], total = 3)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            e'8
            e'8
            f'8
            f'8
            f'8 ]
        }

    Preserve leaf written durations.

    Preserve parentage and spanners.

    Return none.

    .. versionchanged:: 2.0
        renamed ``leaftools.multiply()`` to
        ``leaftools.repeat_leaves_in_expr_and_extend_spanners()``.
    '''

    for leaf in iterate_leaves_backward_in_expr(expr):
        repeat_leaf_and_extend_spanners(leaf, total)
