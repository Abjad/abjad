# -*- coding: utf-8 -*-
from abjad.tools import durationtools


def make_percussion_note(pitch, total_duration, max_note_duration=(1, 8)):
    r'''Makes short note with `max_note_duration` followed
    by rests together totaling `total_duration`.

    ..  container:: example

            >>> leaves = scoretools.make_percussion_note(2, (1, 4), (1, 8))
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                d'8
                r8
            }

    ..  container:: example

            >>> leaves = scoretools.make_percussion_note(2, (1, 64), (1, 8))
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                d'64
            }

    ..  container:: example

            >>> leaves = scoretools.make_percussion_note(2, (5, 64), (1, 8))
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                d'16
                r64
            }

    ..  container:: example

            >>> leaves = scoretools.make_percussion_note(2, (5, 4), (1, 8))
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                d'8
                r1
                r8
            }

    Returns list of newly constructed note followed by zero or
    more newly constructed rests.

    Durations of note and rests returned will sum to `total_duration`.

    Duration of note returned will be no greater than `max_note_duration`.

    Duration of rests returned will sum to note duration taken
    from `total_duration`.

    Useful for percussion music where attack duration is negligible
    and tied notes undesirable.
    '''
    from abjad.tools import scoretools
    from abjad.tools import scoretools
    from abjad.tools import selectiontools

    # check input
    total_duration = durationtools.Duration(total_duration)
    max_note_duration = durationtools.Duration(max_note_duration)

    # make note and rest
    if max_note_duration < total_duration:
        rest_duration = total_duration - max_note_duration
        rests = scoretools.make_tied_leaf(
            scoretools.Rest,
            rest_duration,
            pitches=None,
            )
        notes = scoretools.make_tied_leaf(
            scoretools.Note,
            max_note_duration,
            pitches=pitch,
            )
    else:
        notes = scoretools.make_tied_leaf(
            scoretools.Note,
            total_duration,
            pitches=pitch,
            tie_parts=False,
            )
        if 1 < len(notes):
            new_notes = []
            new_notes.append(notes[0])
            for i in range(1, len(notes)):
                rest = scoretools.Rest(notes[i])
                new_notes.append(rest)
            notes = new_notes
        rests = []

    # return list of percussion note followed by rest
    result = notes + rests
    result = selectiontools.Selection(result)
    return result
