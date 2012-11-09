from abjad.tools import durationtools


def make_leaves_from_talea(talea, denominator, 
    decrease_durations_monotonically=True, tie_rests=False, use_skips=False):
    r'''.. versionadded:: 2.0

    Make leaves from `talea` and `denominator`::

        >>> leaves = leaftools.make_leaves_from_talea([3, -3, 5, -5], 8)
        >>> staff = Staff(leaves)

    ::

        >>> f(staff)
        \new Staff {
            c'4.
            r4.
            c'2 ~
            c'8
            r2
            r8
        }

    Interpret positive elements in `talea` as notes.

    Interpret negative elements in `talea` as rests.

    Set the pitch of all notes to middle C.

    When ``use_skips=False`` use skips instead of rests.

    .. note:: add skip example.

    Return list of notes and / or rests.
    '''
    from abjad.tools import leaftools

    # make notes and rests
    result = []
    for note_value in talea:
        if note_value == 0:
            raise ValueError('note values must be nonzero.')
        elif 0 < note_value:
            leaves = leaftools.make_leaves(
                [0], [durationtools.Duration(note_value, denominator)], 
                decrease_durations_monotonically=decrease_durations_monotonically, 
                tie_rests=tie_rests)
        else:
            leaves = leaftools.make_leaves(
                [None], [durationtools.Duration(-note_value, denominator)],
                decrease_durations_monotonically=decrease_durations_monotonically, 
                tie_rests=tie_rests)
        result.extend(leaves)

    # return result
    return result
