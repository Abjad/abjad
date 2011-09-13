from abjad.tools.notetools.Note import Note
from abjad.tools import durationtools


def make_percussion_note(pitch, total_duration, max_note_duration = (1, 8)):
    '''Make percussion note::

        abjad> notetools.make_percussion_note(2, (1, 4), (1, 8))
        [Note("d'8"), Rest('r8')]

    ::

        abjad> notetools.make_percussion_note(2, (1, 64), (1, 8))
        [Note("d'64")]

    ::

        abjad> notetools.make_percussion_note(2, (5, 64), (1, 8))
        [Note("d'16"), Rest('r64')]

    ::

        abjad> notetools.make_percussion_note(2, (5, 4), (1, 8))
        [Note("d'8"), Rest('r1'), Rest('r8')]

    Return list of newly constructed note followed by zero or more newly constructed rests.

    Durations of note and rests returned will sum to `total_duration`.

    Duration of note returned will be no greater than `max_note_duration`.

    Duration of rests returned will sum to note duration taken from `total_duration`.

    Useful for percussion music where attack duration is negligible and tied notes undesirable.

    .. versionchanged:: 2.0
        renamed ``construct.percussion_note()`` to
        ``notetools.make_percussion_note()``.
    '''
    from abjad.tools.leaftools._construct_tied_leaf import _construct_tied_leaf
    from abjad.tools.leaftools._construct_tied_note import _construct_tied_note
    from abjad.tools.leaftools._construct_tied_rest import _construct_tied_rest
    from abjad.tools.resttools.Rest import Rest

    total_duration = durationtools.Duration(*durationtools.duration_token_to_duration_pair(total_duration))
    max_note_duration = durationtools.Duration(*durationtools.duration_token_to_duration_pair(max_note_duration))

    if max_note_duration < total_duration:
        rest_duration = total_duration - max_note_duration
        r = _construct_tied_rest(rest_duration)
        n = _construct_tied_note(pitch, max_note_duration)
    else:
        #n = _construct_tied_note(pitch, total_duration)
        n = _construct_tied_leaf(Note, total_duration,
            pitches = pitch, tied = False)
        if 1 < len(n):
            for i in range(1, len(n)):
                n[i] = Rest(n[i])
        r = []
    return n + r
