def yield_topmost_components_of_klass_grouped_by_type(expr, klass):
    r'''.. versionadded:: 2.0

    Example 1. Yield runs of topmost notes in `expr`::

        >>> staff = Staff(r"\times 2/3 { c'8 d'8 r8 } \times 2/3 { r8 <e' g'>8 <f' a'>8 }")
        >>> staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'8
                d'8
                r8
            }
            \times 2/3 {
                r8
                <e' g'>8
                <f' a'>8
            }
            g'8
            a'8
            r8
            r8
            <b' d''>8
            <c'' e''>8
        }

    ::
    
        >>> for group in componenttools.yield_topmost_components_of_klass_grouped_by_type(
        ...     staff, Note):
        ...     group
        (Note("g'8"), Note("a'8"))

    Example 2. Yield runs of notes at all levels in `expr`::

        >>> leaves = iterationtools.iterate_leaves_in_expr(staff)

    ::

        >>> for group in componenttools.yield_topmost_components_of_klass_grouped_by_type(
        ...     leaves, Note):
        ...     group
        (Note("c'8"), Note("d'8"))
        (Note("g'8"), Note("a'8"))

    Return generator.
    '''
    from abjad.tools import componenttools

    for group in componenttools.yield_topmost_components_grouped_by_type(expr):
        if isinstance(group[0], klass):
            yield group
