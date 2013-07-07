def partition_components_by_durations_not_greater_than(
    components,
    durations,
    cyclic=False,
    in_seconds=False,
    overhang=False,
    ):
    r'''.. versionadded:: 1.1
    '''
    from abjad.tools.componenttools._partition_components_by_durations \
        import _partition_components_by_durations

    return _partition_components_by_durations(
        components,
        durations,
        fill='less',
        cyclic=cyclic,
        in_seconds=in_seconds,
        overhang=overhang,
        )
