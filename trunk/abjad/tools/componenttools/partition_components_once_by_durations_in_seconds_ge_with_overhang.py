from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations


def partition_components_once_by_durations_in_seconds_ge_with_overhang(
    components, durations_in_seconds):
    '''.. versionadded:: 1.1

    Partition `components` once by durations in seconds that equal
    or are just greater than `durations_in_seconds`, with overhang.
    '''

    parts = _partition_components_by_durations('prolated', components, prolated_duration,
        fill = 'greater', cyclic = False, overhang = True)

    return parts
