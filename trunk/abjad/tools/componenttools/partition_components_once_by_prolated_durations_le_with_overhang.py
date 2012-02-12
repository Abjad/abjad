from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations


def partition_components_once_by_prolated_durations_le_with_overhang(
    components, prolated_durations):
    '''.. versionadded:: 1.1

    Partition `components` once by prolated durations that equal
    or are just less than `prolated_durations`, with overhang.
    '''

    parts = _partition_components_by_durations('prolated', components, prolated_durations,
        fill='less', cyclic=False, overhang=True)

    return parts
