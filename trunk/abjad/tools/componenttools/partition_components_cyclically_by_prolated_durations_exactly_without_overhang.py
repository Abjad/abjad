def partition_components_cyclically_by_prolated_durations_exactly_without_overhang(
    components, prolated_durations):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``componenttools.partition_components_by_durations_exactly()`` instead.

    Partition `components` cyclically by `prolated_durations` exactly, without overhang.
    '''
    from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations

    parts = _partition_components_by_durations('prolated', components, prolated_durations,
        fill='exact', cyclic=True, overhang=False)

    return parts
