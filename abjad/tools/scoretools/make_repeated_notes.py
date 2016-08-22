# -*- coding: utf-8 -*-
from abjad.tools import durationtools


def make_repeated_notes(count, duration=durationtools.Duration(1, 8)):
    r'''Make `count` repeated notes with note head-assignable `duration`:

    ::

        >>> scoretools.make_repeated_notes(4)
        Selection([Note("c'8"), Note("c'8"), Note("c'8"), Note("c'8")])

    Make `count` repeated logical ties with tied `duration`:

    ::

        >>> notes = scoretools.make_repeated_notes(2, (5, 16))
        >>> voice = Voice(notes)

    ..  doctest::

        >>> print(format(voice))
        \new Voice {
            c'4 ~
            c'16
            c'4 ~
            c'16
        }

    Make ad hoc tuplet holding `count` repeated notes with
    non-power-of-two `duration`:

    ::

        >>> scoretools.make_repeated_notes(3, (1, 12))
        Selection([Tuplet(Multiplier(2, 3), "c'8 c'8 c'8")])

    Set pitch of all notes created to middle C.

    Returns list of zero or more newly constructed notes or list
    of one newly constructed tuplet.
    '''
    from abjad.tools import scoretools

    return scoretools.make_notes([0] * count, [duration])
