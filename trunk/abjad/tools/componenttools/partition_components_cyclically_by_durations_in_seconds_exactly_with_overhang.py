from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations


def partition_components_cyclically_by_durations_in_seconds_exactly_with_overhang(
    components, durations_in_seconds):
    '''.. versionadded:: 1.1

    Partition `components` cyclically by `durations_in_seconds` exactly with overhang.
    '''

    parts = _partition_components_by_durations(
        'seconds', components, durations_in_seconds, 'exact', True, True)

    return parts
