from abjad.tools import componenttools


def yield_groups_of_skips_in_sequence(sequence):
    r'''.. versionadded:: 2.0

    Yield groups of skips in `sequence`::

        >>> staff = Staff("c'8 d'8 s8 s8 <e' g'>8 <f' a'>8 g'8 a'8 s8 s8 <b' d''>8 <c'' e''>8")

    ::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            s8
            s8
            <e' g'>8
            <f' a'>8
            g'8
            a'8
            s8
            s8
            <b' d''>8
            <c'' e''>8
        }

    ::

        >>> for skip in skiptools.yield_groups_of_skips_in_sequence(staff):
        ...     skip
        ...
        (Skip('s8'), Skip('s8'))
        (Skip('s8'), Skip('s8'))

    Return generator.
    '''
    from abjad.tools import skiptools

    return componenttools.yield_topmost_components_of_klass_grouped_by_type(sequence, skiptools.Skip)
