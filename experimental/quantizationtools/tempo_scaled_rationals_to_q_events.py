from fractions import Fraction
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from experimental.quantizationtools.PitchedQEvent import PitchedQEvent
from experimental.quantizationtools.SilentQEvent import SilentQEvent
from experimental.quantizationtools.TerminalQEvent import TerminalQEvent
from experimental.quantizationtools.tempo_scaled_rational_to_milliseconds \
    import tempo_scaled_rational_to_milliseconds


def tempo_scaled_rationals_to_q_events(durations, tempo):
    '''Convert a list of rational durations to a list of
    :py:class:`~abjad.tools.quantizationtools.QEvent` objects.

    Negative duration values can be used to indicate silence.  Any resulting
    pitched :py:class:`~abjad.tools.quantizationtools.QEvent` objects will
    default to using middle-C.

    ::

        >>> from experimental import *

    ::

        >>> from experimental.quantizationtools import tempo_scaled_rationals_to_q_events
        >>> durations = [Duration(-1, 2), Duration(1, 4), Duration(1, 6)]
        >>> tempo = contexttools.TempoMark((1, 4), 55)
        >>> for x in tempo_scaled_rationals_to_q_events(durations, tempo): x
        ...
        quantizationtools.SilentQEvent(
            durationtools.Offset(0, 1),
            attachments=()
            )
        quantizationtools.PitchedQEvent(
            durationtools.Offset(24000, 11),
            (NamedChromaticPitch("c'"),),
            attachments=()
            )
        quantizationtools.PitchedQEvent(
            durationtools.Offset(36000, 11),
            (NamedChromaticPitch("c'"),),
            attachments=()
            )
        quantizationtools.TerminalQEvent(
            durationtools.Offset(4000, 1)
            )

    Return a list of :py:class:`~abjad.tools.quantizationtools.QEvent` objects.
    '''

    assert all([isinstance(x, (int, Fraction)) for x in durations])
    assert isinstance(tempo, contexttools.TempoMark)

    durations = [x for x in sequencetools.sum_consecutive_sequence_elements_by_sign(durations, sign=[-1]) if x]
    durations = [tempo_scaled_rational_to_milliseconds(x, tempo) for x in durations]

    offsets = mathtools.cumulative_sums_zero([abs(x) for x in durations])

    q_events = []
    for pair in zip(offsets, durations):
        offset = durationtools.Offset(pair[0])
        duration = pair[1]
        if duration < 0: # negative duration indicates silence
            q_event = SilentQEvent(offset)
        else: # otherwise, use middle-C
            q_event = PitchedQEvent(offset, [0])
        q_events.append(q_event)

    # insert terminating silence QEvent
    q_events.append(TerminalQEvent(offsets[-1]))

    return q_events
