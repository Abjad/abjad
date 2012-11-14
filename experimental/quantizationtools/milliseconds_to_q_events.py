from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools


def milliseconds_to_q_events(milliseconds, fuse_silences=False):
    '''Convert a list of millisecond durations to a list of
    ``QEvent`` instances.

    Negative duration values can be used to indicate silence.  Any resulting
    pitched ``QEvent`` instances will default to using middle-C.

    ::

        >>> durations = [100, -250, 500]
        >>> for x in quantizationtools.milliseconds_to_q_events(durations): x
        ...
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0, 1),
            (NamedChromaticPitch("c'"),),
            attachments=()
            )
        quantizationtools.SilentQEvent(
            durationtools.Offset(100, 1),
            attachments=()
            )
        quantizationtools.PitchedQEvent(
            durationtools.Offset(350, 1),
            (NamedChromaticPitch("c'"),),
            attachments=()
            )
        quantizationtools.TerminalQEvent(
            durationtools.Offset(850, 1)
            )

    Return a list of ``QEvent`` instances.
    '''
    from experimental import quantizationtools

    if fuse_silences:
        durations = [x for x in sequencetools.sum_consecutive_sequence_elements_by_sign(milliseconds, sign=[-1]) if x]
    else:
        durations = milliseconds
    offsets = mathtools.cumulative_sums_zero([abs(x) for x in durations])

    q_events = []
    for pair in zip(offsets, durations):
        offset = durationtools.Offset(pair[0])
        duration = pair[1]
        if duration < 0: # negative duration indicates silence
            q_event = quantizationtools.SilentQEvent(offset)
        else:
            q_event = quantizationtools.PitchedQEvent(offset, [0])
        q_events.append(q_event)

    q_events.append(quantizationtools.TerminalQEvent(durationtools.Offset(offsets[-1])))

    return q_events
