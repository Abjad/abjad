def partition_components_by_durations_not_less_than(
    components,
    durations,
    cyclic=False,
    in_seconds=False,
    overhang=False,
    ):
    r'''.. versionadded:: 1.1

    Partition `components` by `durations` not less than.

    Example 1. Partition `components` cyclically by prolated `durations`. 
    Keep overhang:

    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
        >>> staff.extend("abj: | 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }

    ::

        >>> parts = \
        ...     componenttools.partition_components_by_durations_not_less_than(
        ...     staff.leaves, [Duration(3, 16), Duration(1, 16)], 
        ...     cyclic=True, overhang=True)

    ::

        >>> for part in parts:
        ...     part
        ...
        [Note("c'8"), Note("d'8")]
        [Note("e'8")]
        [Note("f'8"), Note("g'8")]
        [Note("a'8")]
        [Note("b'8"), Note("c''8")]

    Return list of lists.
    '''
    from abjad.tools import componenttools

    return componenttools.partition_components_by_durations(
        components,
        durations,
        cyclic=cyclic,
        fill='greater',
        in_seconds=in_seconds,
        overhang=overhang,
        )
