from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations


def partition_components_cyclically_by_prolated_durations_exactly_without_overhang(
    components, prolated_durations):
    '''.. versionadded:: 1.1

    Partition `components` cyclically by `prolated_durations` exactly, without overhang.
    '''

    parts = _partition_components_by_durations('prolated', components, prolated_durations,
        fill = 'exact', cyclic = True, overhang = False)

    return parts
