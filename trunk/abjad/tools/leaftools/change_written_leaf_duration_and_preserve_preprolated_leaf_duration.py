from abjad.tools import durationtools


def change_written_leaf_duration_and_preserve_preprolated_leaf_duration(leaf, written_duration):
    '''.. versionadded:: 1.1

    Change `leaf` written duration to `written_duration`
    and preserve preprolated `leaf` duration::

        >>> note = Note("c'4")

    ::

        >>> note.written_duration
        Duration(1, 4)
        >>> note.preprolated_duration
        Duration(1, 4)

    ::

        >>> leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
        ...     note, Duration(3, 16))
        Note("c'8. * 4/3")

    ::

        >>> note.written_duration
        Duration(3, 16)
        >>> note.preprolated_duration
        Duration(1, 4)

    Add LilyPond multiplier where necessary.

    Return `leaf`.
    '''
    from abjad.tools import leaftools

    # check leaf type
    if not isinstance(leaf, leaftools.Leaf):
        raise TypeError('must be leaf: %s' % leaf)

    # check written duration type
    written_duration = durationtools.Duration(written_duration)

    # change leaf written duration
    previous = leaf.multiplied_duration
    leaf.written_duration = written_duration

    # change leaf multiplier if required
    leaf.duration_multiplier = None
    multiplier = previous / leaf.written_duration
    if multiplier != 1:
        leaf.duration_multiplier = multiplier

    # return leaf
    return leaf
