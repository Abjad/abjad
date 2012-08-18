def fuse_leaves_in_container_once_by_counts_into_big_endian_notes(container, counts):
    r'''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``leaftools.fuse_leaves_in_container_once_by_counts()``.

    Fuse leaves in `container` once by `counts` into big-endian notes.
    '''
    from abjad.tools import notetools
    from abjad.tools.leaftools.fuse_leaves_in_container_once_by_counts \
        import fuse_leaves_in_container_once_by_counts

    return fuse_leaves_in_container_once_by_counts(container, counts,
        target_type=notetools.Note, big_endian=True)
