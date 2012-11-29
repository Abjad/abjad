def partition_components_by_durations_not_greater_than(components, durations,     
    cyclic=False, in_seconds=False, overhang=False):
    r'''.. versionadded:: 1.1
    '''
    from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations

    if in_seconds:
        duration_type = 'seconds'
    else:
        duration_type = 'prolated'

    return _partition_components_by_durations(duration_type, components, durations,
        fill='less', cyclic=cyclic, overhang=overhang)
