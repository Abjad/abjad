def get_leaf_in_expr_with_minimum_duration(expr):
    r'''.. versionadded:: 2.5

    Get leaf in `expr` with minimum prolated duration::

        >>> staff = Staff("c'4.. d'16 e'4.. f'16")

    ::

        >>> leaftools.get_leaf_in_expr_with_minimum_duration(staff)
        Note("d'16")

    When two leaves in `expr` are both of equally minimal prolated duration,
    return the first leaf encountered in forward iteration.

    Return none when `expr` contains no leaves::

        >>> leaftools.get_leaf_in_expr_with_minimum_duration([]) is None
        True

    Return leaf.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import leaftools

    leaf_with_minimum_prolated_duration = None
    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        if leaf_with_minimum_prolated_duration is None:
            leaf_with_minimum_prolated_duration = leaf
        elif leaf.duration < leaf_with_minimum_prolated_duration.duration:
            leaf_with_minimum_prolated_duration = leaf

    return leaf_with_minimum_prolated_duration
