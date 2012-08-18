def fuse_leaves_in_container_once_by_counts_into_big_endian_notes(container, counts):
    r'''.. versionadded:: 1.1

    Fuse leaves in `container` once by `counts` into big-endian notes.
    '''
    from abjad.tools import notetools
    from abjad.tools.leaftools._fuse_leaves_in_container_once_by_counts \
        import _fuse_leaves_in_container_once_by_counts

    return _fuse_leaves_in_container_once_by_counts(container, counts,
        target_type=notetools.Note, big_endian=True)
