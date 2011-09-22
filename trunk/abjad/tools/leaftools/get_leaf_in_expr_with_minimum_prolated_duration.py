from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def get_leaf_in_expr_with_minimum_prolated_duration(expr):
    r'''.. versionadded:: 2.5

    Get leaf in `expr` with minimum prolated duration::

        abjad> staff = Staff("c'4.. d'16 e'4.. f'16")

    ::

        abjad> leaftools.get_leaf_in_expr_with_minimum_prolated_duration(staff)
        Note("d'16")

    When two leaves in `expr` are both of equally minimal prolated duration,
    return the first leaf encountered in forward iteration.

    Return none when `expr` contains no leaves::
 
        abjad> leaftools.get_leaf_in_expr_with_minimum_prolated_duration([]) is None
        True

    Return leaf.
    '''

    leaf_with_minimum_prolated_duration = None
    for leaf in iterate_leaves_forward_in_expr(expr):
        if leaf_with_minimum_prolated_duration is None:
            leaf_with_minimum_prolated_duration = leaf
        elif leaf.prolated_duration < leaf_with_minimum_prolated_duration.prolated_duration:
            leaf_with_minimum_prolated_duration = leaf

    return leaf_with_minimum_prolated_duration
