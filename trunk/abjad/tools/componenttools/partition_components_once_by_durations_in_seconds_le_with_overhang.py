def partition_components_once_by_durations_in_seconds_le_with_overhang(
    components, durations_in_seconds):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``componenttools.partition_components_by_durations_le()`` instead.

    Partition `components` once by durations in seconds that equal
    or are just less than `durations_in_seconds`, with overhang.
    '''
    from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations

    parts = _partition_components_by_durations('prolated', components, prolated_duration,
        fill='less', cyclic=False, overhang=True)

    return parts
