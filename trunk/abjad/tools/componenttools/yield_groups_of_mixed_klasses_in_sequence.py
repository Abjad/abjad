def yield_groups_of_mixed_klasses_in_sequence(sequence, klasses):
    r'''.. versionadded:: 2.0

    Example 1. Yield groups of notes and chords at only the top level of score::

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

        >>> for group in componenttools.yield_groups_of_mixed_klasses_in_sequence(
        ...     staff, (Note, Chord)):
        ...     group
        (Note("g'8"), Note("a'8"))
        (Chord("<b' d''>8"), Chord("<c'' e''>8"))

    Example 2. Yield groups of notes and chords at all levels of score::

        >>> leaves = iterationtools.iterate_leaves_in_expr(staff)

    ::

        >>> for group in componenttools.yield_groups_of_mixed_klasses_in_sequence(
        ...     leaves, (Note, Chord)):
        ...     group
        (Note("c'8"), Note("d'8"))
        (Chord("<e' g'>8"), Chord("<f' a'>8"), Note("g'8"), Note("a'8"))
        (Chord("<b' d''>8"), Chord("<c'' e''>8"))

    Return generator.
    '''
    from abjad.tools import componenttools

    current_group = ()
    for group in componenttools.yield_topmost_components_grouped_by_type(sequence):
        if type(group[0]) in klasses:
            current_group = current_group + group
        elif current_group:
            yield current_group
            current_group = ()

    if current_group:
        yield current_group
