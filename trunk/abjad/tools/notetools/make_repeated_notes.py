from abjad.tools import durationtools


def make_repeated_notes(count, duration=durationtools.Duration(1, 8)):
    r'''Make `count` repeated notes with note head-assignable `duration`::

        >>> notetools.make_repeated_notes(4)
        [Note("c'8"), Note("c'8"), Note("c'8"), Note("c'8")]

    Make `count` repeated tie chains with tied `duration`::

        >>> notes = notetools.make_repeated_notes(2, (5, 16))
        >>> voice = Voice(notes)

    ::

        >>> f(voice)
        \new Voice {
            c'4 ~
            c'16
            c'4 ~
            c'16
        }

    Make ad hoc tuplet holding `count` repeated notes with non-power-of-two `duration`::

        >>> notetools.make_repeated_notes(3, (1, 12))
        [Tuplet(2/3, [c'8, c'8, c'8])]

    Set pitch of all notes created to middle C.

    Return list of zero or more newly constructed notes or list of one newly constructed tuplet.
    '''
    from abjad.tools import notetools

    return notetools.make_notes([0] * count, [duration])
