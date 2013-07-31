from abjad.tools import componenttools


def fuse_leaves_in_container_once_by_counts(
    container,
    counts,
    leaf_class=None,
    decrease_durations_monotonically=True,
    ):
    r'''Fuse leaves in `container` once by `counts` into 
    instances of `leaf_class`.

    .. note:: add example.
    '''
    from abjad.tools import containertools
    from abjad.tools import notetools
    from abjad.tools import resttools

    if leaf_class is None:
        leaf_class = notetools.Note

    # assert input types
    assert isinstance(container, containertools.Container)

    # assert input values
    if not sum(counts) == len(container):
        raise ValueError('sum of counts must equal length of container.')

    # find preprolated durations of glommed parts of container
    tokens = componenttools.copy_and_partition_governed_component_subtree_by_leaf_counts(
        container, counts)
    durations = [sum([x._preprolated_duration for x in part]) 
        for part in tokens]

    # make new notes or rests
    if leaf_class == notetools.Note:
        new_material = notetools.make_notes(
            0,
            durations,
            decrease_durations_monotonically=decrease_durations_monotonically)
    elif leaf_class == resttools.Rest:
        new_material = resttools.make_rests(
            durations,
            decrease_durations_monotonically=decrease_durations_monotonically)
    else:
        raise ValueError('unknown type of material to construct.')

    # insert new material in container
    container[:] = new_material

    # return container
    return container
