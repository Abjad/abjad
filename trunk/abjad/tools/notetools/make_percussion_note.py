from abjad.tools import durationtools
from abjad.tools import leaftools


def make_percussion_note(pitch, total_duration, max_note_duration=(1, 8)):
    '''.. versionadded:: 1.0

    Make percussion note::

        >>> notetools.make_percussion_note(2, (1, 4), (1, 8))
        [Note("d'8"), Rest('r8')]

    ::

        >>> notetools.make_percussion_note(2, (1, 64), (1, 8))
        [Note("d'64")]

    ::

        >>> notetools.make_percussion_note(2, (5, 64), (1, 8))
        [Note("d'16"), Rest('r64')]

    ::

        >>> notetools.make_percussion_note(2, (5, 4), (1, 8))
        [Note("d'8"), Rest('r1'), Rest('r8')]

    Return list of newly constructed note followed by zero or more newly constructed rests.

    Durations of note and rests returned will sum to `total_duration`.

    Duration of note returned will be no greater than `max_note_duration`.

    Duration of rests returned will sum to note duration taken from `total_duration`.

    Useful for percussion music where attack duration is negligible and tied notes undesirable.
    '''
    from abjad.tools import notetools
    from abjad.tools import resttools

    # check input
    total_duration = durationtools.Duration(total_duration)
    max_note_duration = durationtools.Duration(max_note_duration)

    # make note and rest
    if max_note_duration < total_duration:
        rest_duration = total_duration - max_note_duration
        r = resttools.make_tied_rest(rest_duration)
        n = notetools.make_tied_note(pitch, max_note_duration)
    else:
        n = leaftools.make_tied_leaf(notetools.Note, total_duration, pitches=pitch, tie_parts=False)
        if 1 < len(n):
            for i in range(1, len(n)):
                n[i] = resttools.Rest(n[i])
        r = []

    # return list of percussion note followed by rest
    return n + r
