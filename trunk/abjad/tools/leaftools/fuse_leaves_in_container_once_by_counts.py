from abjad.tools import componenttools


def fuse_leaves_in_container_once_by_counts(container, counts, klass=None, big_endian=True):
    '''Fuse leaves in `container` once by `counts` into instances of `klass`.
    '''
    from abjad.tools import containertools
    from abjad.tools import notetools
    from abjad.tools import resttools

    if klass is None:
        klass = notetools.Note

    # assert input types
    assert isinstance(container, containertools.Container)

    # assert input values
    if not sum(counts) == len(container):
        raise ValueError('sum of counts must equal length of container.')

    # find preprolated durations of glommed parts of container
    tokens = componenttools.copy_and_partition_governed_component_subtree_by_leaf_counts(
        container, counts)
    durations = [sum([x.preprolated_duration for x in part]) for part in tokens]

    # construct new notes or rests
    if klass == notetools.Note:
        new_material = notetools.make_notes(0, durations, big_endian=big_endian)
    elif klass == resttools.Rest:
        new_material = resttools.make_rests(durations, big_endian=big_endian)
    else:
        raise ValueError('unknown type of material to construct.')

    # insert new material in container
    container[:] = new_material

    # return container
    return container
