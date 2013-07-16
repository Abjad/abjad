import itertools


def yield_components_grouped_by_duration(components):
    r'''.. versionadded:: 2.0

    Example 1. Yield topmost components grouped by prolated duration:

    ::

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

        >>> show(staff) # doctest: +SKIP

    ::

        >>> for x in componenttools.yield_components_grouped_by_duration(staff):
        ...     x
        ...
        (Tuplet(2/3, [c'4, c'4, c'8, c'16, c'16]),)
        (Note("c'16"), Note("c'16"))
        (Note("c'8"), Note("c'8"))

    Example 2. Yield topmost components grouped by prolated duration.

    Note that function treats input as a flat sequence and
    attempts no navigation of the score tree.
    But it's possible to group components lower in the score tree by passing
    the output of a component iterator as input to this function:

    ::

        >>> staff = Staff(r"\times 2/3 { c'4 c'4 c'8 c'16 c'16 } c'16 c'16 c'8 c'8")

    ::

        >>> leaves = iterationtools.iterate_leaves_in_expr(staff)
        >>> for x in componenttools.yield_components_grouped_by_duration(leaves):
        ...     x
        (Note("c'4"), Note("c'4"))
        (Note("c'8"),)
        (Note("c'16"), Note("c'16"))
        (Note("c'16"), Note("c'16"))
        (Note("c'8"), Note("c'8"))

    Return generator.
    '''

    grouper = itertools.groupby(components, lambda x: x.duration)
    for duration, generator in grouper:
        yield tuple(generator)
