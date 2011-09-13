from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools import durationtools


def change_written_leaf_duration_and_preserve_preprolated_leaf_duration(leaf, written_duration):
    '''.. versionadded:: 1.1

    Change `leaf` written duration to `written_duration` and preserve preprolated `leaf` duration::

        abjad> note = Note("c'4")
        abjad> note.written_duration
        Duration(1, 4)
        abjad> note.preprolated_duration
        Duration(1, 4)

    ::

        abjad> leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(note, Duration(3, 16))
        Note("c'8. * 4/3")

    ::

        abjad> note.written_duration
        Duration(3, 16)
        abjad> note.preprolated_duration
        Duration(1, 4)

    Add LilyPond multiplier where necessary.

    Return `leaf`.

    .. versionchanged:: 2.0
        Renamed from ``leaftools.duration_rewrite()``.
        ``leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration()``.
    '''

    # check leaf type
    if not isinstance(leaf, _Leaf):
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
