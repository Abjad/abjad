def _fuse_leaves_in_container_once_by_counts(container, counts, target_type = None, direction = 'big-endian'):
    '''Fuse leaves in `container` once by `counts` into `direction`-oriented
    instances of `target_type`.
    '''
    from abjad.tools.containertools.Container import Container
    from abjad.tools.notetools.Note import Note
    from abjad.tools.resttools.Rest import Rest
    from abjad.tools import componenttools
    from abjad.tools import notetools
    from abjad.tools import resttools

    if target_type is None:
        target_type = Note

    # assert input types
    assert isinstance(container, Container)

    # assert input values
    if not sum(counts) == len(container):
        raise ValueError('sum of counts must equal length of container.')

    # find preprolated durations of glommed parts of container
    tokens = componenttools.copy_and_partition_governed_component_subtree_by_leaf_counts(
        container, counts)
    durations = [sum([x.preprolated_duration for x in part]) for part in tokens]

    # construct new notes or rests
    if target_type == Note:
        new_material = notetools.make_notes(0, durations, direction = direction)
    elif target_type == Rest:
        new_material = resttools.make_rests(durations, direction = direction)
    else:
        raise ValueError('unknown type of material to construct.')

    # insert new material in container
    container[:] = new_material

    # return container
    return container
