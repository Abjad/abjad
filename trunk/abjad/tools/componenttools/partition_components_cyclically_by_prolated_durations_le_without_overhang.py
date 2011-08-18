from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations


def partition_components_cyclically_by_prolated_durations_le_without_overhang(
    components, prolated_durations):
    '''.. versionadded:: 1.1

    Partition `components` cyclically by prolated durations that equal
    or are just less than `prolated_durations`, without overhang.
    '''

    parts = _partition_components_by_durations('prolated', components, prolated_durations,
        fill = 'less', cyclic = True, overhang = False)

    return parts
