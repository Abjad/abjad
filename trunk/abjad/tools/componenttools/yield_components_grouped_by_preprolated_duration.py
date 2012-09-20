def yield_components_grouped_by_preprolated_duration(components):
    r'''.. versionadded:: 2.0

    Example 1. Yield topmost components grouped by preprolated duration::

        >>> staff = Staff(r"\times 2/3 { c'4 c'4 c'8 c'16 c'16 } c'16 c'16 c'8 c'8")

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'4
                c'4
                c'8
                c'16
                c'16
            }
            c'16
            c'16
            c'8
            c'8
        }

    ::

        >>> for x in componenttools.yield_components_grouped_by_preprolated_duration(staff):
        ...     x
        ...
        (Tuplet(2/3, [c'4, c'4, c'8, c'16, c'16]),)
        (Note("c'16"), Note("c'16"))
        (Note("c'8"), Note("c'8"))


    Example 2. Yield topmost components grouped by preprolated duration.

    Note that function treats input as a flat sequence and 
    attempts no navigation of the score tree.
    But it's possible to group components lower in the score tree by passing
    the output of a component iterator as input to this function::

        >>> staff = Staff(r"\times 2/3 { c'4 c'4 c'8 c'16 c'16 } c'16 c'16 c'8 c'8")

    ::

        >>> leaves = iterationtools.iterate_leaves_in_expr(staff)
        >>> for x in componenttools.yield_components_grouped_by_preprolated_duration(leaves):
        ...     x
        (Note("c'4"), Note("c'4"))
        (Note("c'8"),)
        (Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"))
        (Note("c'8"), Note("c'8"))

    Return generator.
    
    .. note:: Might be best to add ``in_sequence`` or ``topmost`` to the name
        of this function.
    '''

    current_group = []
    for component in components:
        if current_group:
            previous_component = current_group[-1]
            prev_duration = previous_component.preprolated_duration
            current_duration = component.preprolated_duration
            if current_duration == prev_duration:
                current_group.append(component)
            else:
                yield tuple(current_group)
                current_group = []
                current_group.append(component)
        else:
            current_group.append(component)
    if current_group:
        yield tuple(current_group)
