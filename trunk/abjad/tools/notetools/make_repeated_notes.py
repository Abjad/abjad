from abjad.tools.notetools.make_notes import make_notes
from abjad.tools import durationtools


def make_repeated_notes(count, duration = durationtools.Duration(1, 8)):
    r'''Make `count` repeated notes with note head-assignable `duration`::

        abjad> notetools.make_repeated_notes(4)
        [Note("c'8"), Note("c'8"), Note("c'8"), Note("c'8")]

    Make `count` repeated tie chains with tied `duration`::

        abjad> notes = notetools.make_repeated_notes(2, (5, 16))
        abjad> voice = Voice(notes)

    ::

        abjad> f(voice)
        \new Voice {
            c'4 ~
            c'16
            c'4 ~
            c'16
        }

    Make ad hoc tuplet holding `count` repeated notes with nonbinary `duration`::

        abjad> notetools.make_repeated_notes(3, (1, 12))
        [Tuplet(2/3, [c'8, c'8, c'8])]

    Set pitch of all notes created to middle C.

    Return list of zero or more newly constructed notes or list of one newly constructed tuplet.

    .. versionchanged:: 2.0
        renamed ``construct.run()`` to
        ``notetools.make_repeated_notes()``.
    '''

    return make_notes([0] * count, [duration])
