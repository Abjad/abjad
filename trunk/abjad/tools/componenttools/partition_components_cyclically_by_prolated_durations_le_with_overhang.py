def partition_components_cyclically_by_prolated_durations_le_with_overhang(
    components, prolated_durations):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``componenttools.partition_components_by_durations_le()`` instead.

    Partition `components` cyclically by prolated duration that equal
    or are just less than `prolated_durations`, with overhang.
    '''
    from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations

    parts = _partition_components_by_durations('prolated', components, prolated_durations,
        fill='less', cyclic=True, overhang=True)

    return parts
