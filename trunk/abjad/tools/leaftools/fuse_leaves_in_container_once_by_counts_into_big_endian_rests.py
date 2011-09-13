def fuse_leaves_in_container_once_by_counts_into_big_endian_rests(container, counts):
    '''.. versionadded:: 1.1

    Fuse leaves in `container` once by `counts` into big-endian rests.
    '''
    from abjad.tools.resttools.Rest import Rest
    from abjad.tools.leaftools._fuse_leaves_in_container_once_by_counts \
        import _fuse_leaves_in_container_once_by_counts

    return _fuse_leaves_in_container_once_by_counts(container, counts,
        target_type = Rest, direction = 'big-endian')
