def partition_components_cyclically_by_prolated_durations_ge_without_overhang(
    components, prolated_durations):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``componenttools.partition_components_by_durations_ge()`` instead.

    Partition `components` cyclically by prolated durations that equal
    or are just greater than `prolated_durations`, without overhang.
    '''
    from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations

    parts = _partition_components_by_durations('prolated', components, prolated_duration,
        fill='greater', cyclic=True, overhang=False)

    return parts
