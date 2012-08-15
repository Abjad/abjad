from abjad.tools import durationtools


def make_leaves_from_note_value_signal(note_value_signal, denominator_of_signal, 
    tie_rests=False, use_skips=False):
    r'''.. versionadded:: 2.0

    Make leaves from `note_value_signal` and `denominator_of_signal`::

        >>> leaves = leaftools.make_leaves_from_note_value_signal([3, -3, 5, -5], 8)
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

    Interpret positive elements in `note_value_signal` as notes.

    Interpret negative elements in `note_value_signal` as rests.

    Set the pitch of all notes to middle C.

    When ``use_skips=False`` use skips instead of rests.

    .. note:: Add skip example.

    Return list of notes and / or rests.
    '''
    from abjad.tools import leaftools

    result = []

    for note_value in note_value_signal:
        if note_value == 0:
            raise ValueError('note values must be nonzero.')
        elif 0 < note_value:
            leaves = leaftools.make_leaves([0], [durationtools.Duration(note_value, denominator_of_signal)])
        else:
            leaves = leaftools.make_leaves([None], [durationtools.Duration(-note_value, denominator_of_signal)],
                tie_rests = tie_rests)
        result.extend(leaves)

    return result
