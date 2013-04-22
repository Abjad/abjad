from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools


def tempo_scaled_durations_to_q_events(durations, tempo):
    '''Convert a list of rational durations to a list of
    ``QEvent`` instances.

    Negative duration values can be used to indicate silence.  Any resulting
    pitched ``QEvents`` will default to using middle-C.

    ::

        >>> durations = [Duration(-1, 2), Duration(1, 4), Duration(1, 6)]
        >>> tempo = contexttools.TempoMark((1, 4), 55)
        >>> for x in quantizationtools.tempo_scaled_durations_to_q_events(
        ...     durations, tempo): x
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

    Return a list of ``QEvent`` instances.
    '''
    from abjad.tools import quantizationtools

    durations = [durationtools.Duration(x) for x in durations]
    assert isinstance(tempo, contexttools.TempoMark)

    durations = [x for x in sequencetools.sum_consecutive_sequence_elements_by_sign(durations, sign=[-1]) if x]
    durations = [quantizationtools.tempo_scaled_duration_to_milliseconds(x, tempo) for x in durations]

    offsets = mathtools.cumulative_sums_zero([abs(x) for x in durations])

    q_events = []
    for pair in zip(offsets, durations):
        offset = durationtools.Offset(pair[0])
        duration = pair[1]
        if duration < 0: # negative duration indicates silence
            q_event = quantizationtools.SilentQEvent(offset)
        else: # otherwise, use middle-C
            q_event = quantizationtools.PitchedQEvent(offset, [0])
        q_events.append(q_event)

    # insert terminating silence QEvent
    q_events.append(quantizationtools.TerminalQEvent(offsets[-1]))

    return q_events
