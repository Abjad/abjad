def partition_components_cyclically_by_durations_in_seconds_exactly_with_overhang(
    components, durations_in_seconds):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``componenttools.partition_components_by_durations_exactly()`` instead.

    Partition `components` cyclically by `durations_in_seconds` exactly with overhang.
    '''
    from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations

    parts = _partition_components_by_durations('seconds', components, durations_in_seconds, 
        fill='exact', cyclic=True, overhang=True)

    return parts
