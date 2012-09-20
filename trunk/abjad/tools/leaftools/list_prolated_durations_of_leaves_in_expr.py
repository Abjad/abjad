def list_prolated_durations_of_leaves_in_expr(expr):
    '''.. versionadded:: 2.0

    List prolated durations of leaves in `expr`::

        >>> staff = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { c'8 d'8 e'8 }")

    ::

        >>> for duration in leaftools.list_prolated_durations_of_leaves_in_expr(staff):
        ...     duration
        ...
        Duration(1, 12)
        Duration(1, 12)
        Duration(1, 12)
        Duration(1, 12)
        Duration(1, 12)
        Duration(1, 12)

    Return list of durations.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import leaftools

    durations = []

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        durations.append(leaf.prolated_duration)

    return durations
