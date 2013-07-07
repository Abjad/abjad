def partition_components_by_durations_exactly(
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
        fill='exact',
        cyclic=cyclic,
        in_seconds=in_seconds,
        overhang=overhang,
        )
