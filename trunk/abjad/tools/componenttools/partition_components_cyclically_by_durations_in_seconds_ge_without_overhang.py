from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations


def partition_components_cyclically_by_durations_in_seconds_ge_without_overhang(
    components, durations_in_seconds):
    '''.. versionadded:: 1.1

    Partition `components` cyclically by durations in seconds that are
    equal to or just greater than `durations_in_seconds`, without overhang.
    '''

    parts = _partition_components_by_durations('prolated', components, prolated_duration,
        fill = 'greater', cyclic = True, overhang = False)

    return parts
