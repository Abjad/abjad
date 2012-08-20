def partition_components_by_durations_ge(components, durations,     
    cyclic=False, in_seconds=False, overhang=False):
    r'''.. versionadded:: 1.1

    Partition `components` by `durations`.

    Example 1. Partition `components` cyclically by prolated `durations`. Keep overhang::

        >>> string = "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
        >>> staff = Staff(string)

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

        >>> parts = componenttools.partition_components_by_durations_ge(
        ...     staff.leaves, [Duration(3, 16), Duration(1, 16)], cyclic=True, overhang=True)

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

    Function works not just on components but on any durated objects including spanners.
    '''
    from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations

    if in_seconds:
        duration_type = 'seconds'
    else:
        duration_type = 'prolated'

    return _partition_components_by_durations(duration_type, components, durations,
        fill='greater', cyclic=cyclic, overhang=overhang)
