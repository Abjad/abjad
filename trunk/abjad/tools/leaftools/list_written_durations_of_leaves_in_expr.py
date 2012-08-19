def list_written_durations_of_leaves_in_expr(expr):
    '''.. versionadded:: 2.0

    List the written durations of leaves in `expr`::

        >>> staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8") * 2)

    ::

        >>> for duration in leaftools.list_written_durations_of_leaves_in_expr(staff):
        ...     duration
        ...
        Duration(1, 8)
        Duration(1, 8)
        Duration(1, 8)
        Duration(1, 8)
        Duration(1, 8)    
         Duration(1, 8)

    Return list of durations.
    '''
    from abjad.tools import leaftools

    durations = []

    for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
        durations.append(leaf.written_duration)

    return durations
