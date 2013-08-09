# -*- encoding: utf-8 -*-


def partition_components_by_durations_exactly(
    components,
    durations,
    cyclic=False,
    in_seconds=False,
    overhang=False,
    ):
    from abjad.tools import componenttools

    return componenttools.partition_components_by_durations(
        components,
        durations,
        cyclic=cyclic,
        fill='exact',
        in_seconds=in_seconds,
        overhang=overhang,
        )
