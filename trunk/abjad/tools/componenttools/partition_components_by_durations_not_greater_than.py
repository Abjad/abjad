def partition_components_by_durations_not_greater_than(
    components,
    durations,
    cyclic=False,
    in_seconds=False,
    overhang=False,
    ):
    r'''.. versionadded:: 1.1
    '''
    from abjad.tools import componenttools

    return componenttools.partition_components_by_durations(
        components,
        durations,
        cyclic=cyclic,
        fill='less',
        in_seconds=in_seconds,
        overhang=overhang,
        )
