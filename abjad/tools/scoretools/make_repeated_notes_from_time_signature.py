# -*- coding: utf-8 -*-
from abjad.tools import selectiontools


def make_repeated_notes_from_time_signature(time_signature, pitch="c'"):
    '''Make repeated notes from `time_signature`:

    ::

        >>> scoretools.make_repeated_notes_from_time_signature((5, 32))
        Selection([Note("c'32"), Note("c'32"), Note("c'32"), Note("c'32"), Note("c'32")])

    Make repeated notes with `pitch` from `time_signature`:

    ::

        >>> scoretools.make_repeated_notes_from_time_signature((5, 32), pitch="d''")
        Selection([Note("d''32"), Note("d''32"), Note("d''32"), Note("d''32"), Note("d''32")])

    Returns list of notes.
    '''
    from abjad.tools import indicatortools
    from abjad.tools import scoretools

    # afford basic input polymorphism
    time_signature = indicatortools.TimeSignature(time_signature)

    # check input
    if time_signature.has_non_power_of_two_denominator:
        raise NotImplementedError(
            'TODO: extend this function for time signatures with a non-power-of-two denominators.')

    # make and return repeated notes
    duration = (1, time_signature.denominator)
    result = time_signature.numerator * scoretools.Note(pitch, duration)

    # return result
    result = selectiontools.Selection(result)
    return result
