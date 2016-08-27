# -*- coding: utf-8 -*-
from abjad.tools import selectiontools


def make_repeated_notes_from_time_signatures(time_signatures, pitch="c'"):
    '''Make repated notes from `time_signatures`:

    ::

        scoretools.make_repeated_notes_from_time_signatures([(2, 8), (3, 32)])
        [Selection(Note("c'8"), Note("c'8")), Selection(Note("c'32"), Note("c'32"), Note("c'32"))]

    Make repeated notes with `pitch` from `time_signatures`:

    ::

        >>> for x in scoretools.make_repeated_notes_from_time_signatures(
        ...     [(2, 8), (3, 32)], pitch="d''"):
        ...     x
        ...
        Selection([Note("d''8"), Note("d''8")])
        Selection([Note("d''32"), Note("d''32"), Note("d''32")])

    Returns two-dimensional list of note lists.

    Use ``sequencetools.flatten_sequence()`` to flatten output if required.
    '''
    from abjad.tools import scoretools

    # init result
    result = []

    # iterate time signatures and make notes
    for time_signature in time_signatures:
        notes = scoretools.make_repeated_notes_from_time_signature(
            time_signature, pitch=pitch)
        result.append(notes)

    # return result
    return result
